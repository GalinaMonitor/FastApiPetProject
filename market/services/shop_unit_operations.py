from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy.future import select
from sqlalchemy_continuum import version_class
from sqlmodel.ext.asyncio.session import AsyncSession

from market import tables
from market.api.error_handler import NotFoundException
from market.database import get_session
from market.models.operations import ShopUnitImportRequest, ShopUnitStatisticResponse
from market.tables import ShopUnit

from datetime import datetime, timedelta


class ShopUnitService:
	def __init__(self, session: AsyncSession = Depends(get_session)):
		self.session = session

	async def get_shop_unit(self, id: UUID) -> ShopUnit:
		shop_unit = await self.session.execute(select(tables.ShopUnit).where(tables.ShopUnit.id == id.__str__()))
		shop_unit = shop_unit.scalars().first()
		if not shop_unit:
			raise NotFoundException()
		return shop_unit

	async def get_shop_unit_with_datefilter(self, dt: datetime) -> ShopUnitStatisticResponse:
		return ShopUnitStatisticResponse(items=self.session.query(tables.ShopUnit).filter(dt - tables.ShopUnit.date <= timedelta(hours=24)).all())

	async def get_shop_unit_statistic(self, id: UUID, date_start: datetime, date_end: datetime) -> ShopUnitStatisticResponse:
		ShopUnitVersion = version_class(tables.ShopUnit)
		query = self.session.query(ShopUnitVersion).filter(
			ShopUnitVersion.id == id.__str__()
		)
		if date_start:
			query = query.filter(ShopUnitVersion.date >= date_start)
		if date_end:
			query = query.filter(ShopUnitVersion.date <= date_end)
		return ShopUnitStatisticResponse(items=query.all())


	async def delete_shop_unit(self, id: UUID) -> None:
		shop_unit = self.session.query(tables.ShopUnit).get(id.__str__())
		if not shop_unit:
			raise NotFoundException()
		self.session.delete(shop_unit)
		self.session.commit()

	async def import_shop_units(self, shop_units: ShopUnitImportRequest) -> None:
		for shop_unit in shop_units.items:
			shop_dict = shop_unit.dict()
			shop_dict['date'] = shop_units.updateDate
			shop_dict['id'] = shop_unit.id.__str__()
			if shop_dict['parentId']:
				parent = self.session.query(tables.ShopUnit).get(shop_dict['parentId'].__str__())
				if not parent:
					raise NotFoundException()
				if parent.type != 'CATEGORY':
					raise RequestValidationError(errors=[ErrorWrapper(exc=ValueError(), loc=('parentId',))])
			existed_shop_unit = self.session.query(tables.ShopUnit).get(shop_dict['id'].__str__())
			if existed_shop_unit:
				for param, value in shop_dict.items():
					setattr(existed_shop_unit, param, value)
			else:
				operation = tables.ShopUnit(**shop_dict)
				self.session.add(operation)
			self.session.commit()
