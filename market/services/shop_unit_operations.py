from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from market.api.error_handler import NotFoundException
from market.db.database import get_session
from market.models.operations import ShopUnitImportRequest, ShopUnitStatisticResponse
from market.models.operations import ShopUnitDB

from datetime import datetime, timedelta


class ShopUnitService:
	def __init__(self, session: AsyncSession = Depends(get_session)):
		self.session = session

	async def get_shop_unit(self, id: UUID) -> ShopUnitDB:
		statement = select(ShopUnitDB).where(ShopUnitDB.id == id.__str__()).options(joinedload(ShopUnitDB.children))
		results = await self.session.exec(statement)
		shop_unit = results.first()
		if not shop_unit:
			raise NotFoundException()
		return shop_unit

	async def get_shop_unit_with_datefilter(self, dt: datetime) -> ShopUnitStatisticResponse:
		statement = select(ShopUnitDB).where(dt - ShopUnitDB.date <= timedelta(hours=24))
		results = await self.session.scalars(statement)
		return ShopUnitStatisticResponse(items=results.all())

	async def delete_shop_unit(self, id: UUID) -> None:
		statement = select(ShopUnitDB).where(ShopUnitDB.id == id.__str__())
		results = await self.session.scalars(statement)
		shop_unit = results.first()
		if not shop_unit:
			raise NotFoundException()
		await self.session.delete(shop_unit)
		await self.session.commit()

	async def import_shop_units(self, shop_units: ShopUnitImportRequest) -> None:
		for shop_unit in shop_units.items:
			shop_dict = shop_unit.dict()
			shop_dict['date'] = shop_units.updateDate
			shop_dict['id'] = shop_unit.id.__str__()
			if shop_dict['parentId']:
				statement = select(ShopUnitDB).where(ShopUnitDB.id == shop_dict['parentId'].__str__())
				results = await self.session.scalars(statement)
				parent = results.first()
				if not parent:
					raise NotFoundException()
				if parent.type != 'CATEGORY':
					raise RequestValidationError(errors=[ErrorWrapper(exc=ValueError(), loc=('parentId',))])
			statement = select(ShopUnitDB).where(ShopUnitDB.id == shop_dict['id'].__str__())
			results = await self.session.scalars(statement)
			existed_shop_unit = results.first()
			if existed_shop_unit:
				for param, value in shop_dict.items():
					setattr(existed_shop_unit, param, value)
			else:
				operation = ShopUnitDB(**shop_dict)
				self.session.add(operation)
			await self.session.commit()
