from fastapi import APIRouter, Depends, Query

from datetime import datetime
from typing import Union, Optional
from uuid import UUID

from market.models.operations import Error, ShopUnit, ShopUnitImportRequest, ShopUnitStatisticResponse
from market.services.shop_unit_operations import ShopUnitService

router = APIRouter()


@router.delete(
	'/delete/{id}',
	response_model=None,
	responses={'400': {'model': Error}, '404': {'model': Error}},
)
async def delete_delete_id(id: UUID, service: ShopUnitService = Depends()) -> Union[None, Error]:
	return await service.delete_shop_unit(id)


@router.post('/imports', response_model=None, responses={'400': {'model': Error}})
async def post_imports(body: ShopUnitImportRequest = None, service: ShopUnitService = Depends()) -> Union[None, Error]:
	return await service.import_shop_units(body)


@router.get(
	'/nodes/{id}',
	response_model=ShopUnit,
	responses={'400': {'model': Error}, '404': {'model': Error}},
)
async def get_nodes_id(id: UUID, service: ShopUnitService = Depends()) -> Union[ShopUnit, Error]:
	return await service.get_shop_unit(id)


@router.get(
	'/sales',
	response_model=ShopUnitStatisticResponse,
	responses={'400': {'model': Error}},
)
async def get_sales(date: datetime, service: ShopUnitService = Depends()) -> Union[ShopUnitStatisticResponse, Error]:
	return await service.get_shop_unit_with_datefilter(date)


@router.get(
	'/node/{id}/statistic',
	response_model=ShopUnitStatisticResponse,
	responses={'400': {'model': Error}, '404': {'model': Error}},
)
async def get_node_id_statistic(
		id: UUID,
		service: ShopUnitService = Depends(),
		date_start: Optional[datetime] = Query(None, alias='dateStart'),
		date_end: Optional[datetime] = Query(None, alias='dateEnd'),
) -> Union[ShopUnitStatisticResponse, Error]:
	return await service.get_shop_unit_statistic(id, date_start, date_end)
