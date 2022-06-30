import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy_continuum import make_versioned

from market.models.operations import ShopUnitType

Base = declarative_base()

make_versioned(user_cls=None)

class ShopUnit(Base):
	__versioned__ = {}
	__tablename__ = 'shop_unit'

	id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	price = sqlalchemy.Column(sqlalchemy.Integer)
	date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
	type = sqlalchemy.Column(sqlalchemy.Enum(ShopUnitType))
	parentId = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('shop_unit.id'), nullable=True)
	children = relationship('ShopUnit', backref=backref('parent', remote_side=[id]), cascade='all, delete')


sqlalchemy.orm.configure_mappers()
