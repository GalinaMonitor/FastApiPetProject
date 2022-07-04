import enum
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import backref, RelationshipProperty
from sqlmodel import SQLModel, Field, Relationship


class ShopUnitType(str, enum.Enum):
	OFFER = 'OFFER'
	CATEGORY = 'CATEGORY'


class MyBaseModel(SQLModel):
	class Config:
		orm_mode = True
		json_encoders = {
			datetime: lambda dt: dt.isoformat()
		}


class ShopUnitBase(SQLModel):
	id: UUID = Field(primary_key=True)
	name: str
	price: int
	date: datetime
	type: ShopUnitType
	parentId: Optional[UUID] = Field(
		sa_column=Column(
			"parentId",
			ForeignKey("shop_unit.id"),
			nullable=True,
		)
	)


class ShopUnitDB(ShopUnitBase, table=True):
	id: UUID = Field(primary_key=True)
	name: str
	price: int
	date: datetime
	type: ShopUnitType
	parentId: Optional[UUID] = Field(
		sa_column=Column(
			"parentId",
			ForeignKey("shopunitdb.id"),
			nullable=True,
		)
	)
	children: List['ShopUnitDB'] = Relationship(
		sa_relationship=RelationshipProperty(
			"ShopUnitDB",
			backref=backref('parent', remote_side="ShopUnitDB.id"),
			cascade='all, delete-orphan',
			lazy='joined',
		)
	)


class ShopUnitDBRead(ShopUnitBase):
	children: List['ShopUnitDB'] = []


class ShopUnit(MyBaseModel):
	id: UUID = Field(
		...,
		description='Уникальный идентфикатор',
	)
	name: str = Field(..., description='Имя категории')
	date: datetime = Field(
		...,
		description='Время последнего обновления элемента.',
	)
	parentId: Optional[UUID] = Field(
		None,
		description='UUID родительской категории',
	)
	type: ShopUnitType
	price: Optional[int] = Field(
		None,
		description='Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null.',
	)
	children: Optional[List['ShopUnit']] = Field(
		None,
		description='Список всех дочерних товаров\\категорий. Для товаров поле равно null.',
	)

	class Config:
		orm_mode = True


class ShopUnitImport(MyBaseModel):
	id: UUID = Field(
		...,
		description='Уникальный идентфикатор',
	)
	name: str = Field(..., description='Имя элемента.')
	parentId: Optional[UUID] = Field(
		None,
		description='UUID родительской категории',
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
	)

	class Config:
		orm_mode = True


class ShopUnitStatisticUnit(MyBaseModel):
	id: UUID = Field(
		...,
		description='Уникальный идентфикатор',
	)
	name: str = Field(..., description='Имя элемента')
	parentId: Optional[UUID] = Field(
		None,
		description='UUID родительской категории',
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


class Error(SQLModel):
	code: int
	message: str
