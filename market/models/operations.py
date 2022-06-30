from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ShopUnitType(str, enum.Enum):
	OFFER = 'OFFER'
	CATEGORY = 'CATEGORY'

class MyBaseModel(BaseModel):
	class Config:
		orm_mode = True
		json_encoders = {
			datetime: lambda dt: dt.isoformat()
		}



class ShopUnit(MyBaseModel):
	id: UUID = Field(
		...,
		description='Уникальный идентфикатор',
		example='3fa85f64-5717-4562-b3fc-2c963f66a333',
	)
	name: str = Field(..., description='Имя категории')
	date: datetime = Field(
		...,
		description='Время последнего обновления элемента.',
		example='2022-05-28T21:12:01.000Z',
	)
	parentId: Optional[UUID] = Field(
		None,
		description='UUID родительской категории',
		example='3fa85f64-5717-4562-b3fc-2c963f66a333',
	)
	type: ShopUnitType
	price: Optional[int] = Field(
		None,
		description='Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null.',
	)
	children: Optional[List[ShopUnit]] = Field(
		None,
		description='Список всех дочерних товаров\\категорий. Для товаров поле равно null.',
	)

	class Config:
		orm_mode = True



class ShopUnitImport(MyBaseModel):
	id: UUID = Field(
		...,
		description='Уникальный идентфикатор',
		example='3fa85f64-5717-4562-b3fc-2c963f66a333',
	)
	name: str = Field(..., description='Имя элемента.')
	parentId: Optional[UUID] = Field(
		None,
		description='UUID родительской категории',
		example='3fa85f64-5717-4562-b3fc-2c963f66a333',
	)
	type: ShopUnitType
	price: Optional[int] = Field(
		None, description='Целое число, для категорий поле должно содержать null.'
	)
	class Config:
		orm_mode = True


class ShopUnitImportRequest(MyBaseModel):
	items: Optional[List[ShopUnitImport]] = Field(
		None, description='Импортируемые элементы'
	)
	updateDate: Optional[datetime] = Field(
		None,
		description='Время обновления добавляемых товаров/категорий.',
		example='2022-05-28T21:12:01.000Z',
	)
	class Config:
		orm_mode = True


class ShopUnitStatisticUnit(MyBaseModel):
	id: UUID = Field(
		...,
		description='Уникальный идентфикатор',
		example='3fa85f64-5717-4562-b3fc-2c963f66a333',
	)
	name: str = Field(..., description='Имя элемента')
	parentId: Optional[UUID] = Field(
		None,
		description='UUID родительской категории',
		example='3fa85f64-5717-4562-b3fc-2c963f66a333',
	)
	type: ShopUnitType
	price: Optional[int] = Field(
		None,
		description='Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null.',
	)
	date: datetime = Field(..., description='Время последнего обновления элемента.')

	class Config:
		orm_mode = True


class ShopUnitStatisticResponse(MyBaseModel):
	items: Optional[List[ShopUnitStatisticUnit]] = Field(
		None, description='История в произвольном порядке.'
	)

	class Config:
		orm_mode = True


class Error(BaseModel):
	code: int
	message: str
