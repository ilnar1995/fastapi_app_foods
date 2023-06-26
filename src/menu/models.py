from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Session, selectinload, joinedload, aliased, subqueryload, contains_eager, contains_alias
from src.core.db import Base
from sqlalchemy.exc import IntegrityError, NoResultFound
from .exceptions import DuplicatedEntryError
from src.menu.schemas import FoodCategoryCreate, FoodCreate, ToppingCreate, FoodList
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy import select, delete, update, insert
from . import mixins


class Topping(Base):
    __tablename__ = "topping"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name: str = Column(String(350), unique=True)

    foods = relationship("Food", secondary='food_topping', back_populates="toppings")

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls).order_by(cls.id)  # .options(selectinload(cls.user)) для стягивания модели user при загрузке
        return (await session.execute(query)).scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, item: ToppingCreate):
        new_post = cls(**item.dict())
        session.add(new_post)
        try:
            await session.commit()  # чтоб транзакция завершилась
            await session.refresh(new_post)
            return new_post
        except IntegrityError as ex:
            await session.rollback()
            raise DuplicatedEntryError("The post is already stored")


toppings = Topping.__table__


class Food(Base, mixins.ModelMixin):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description: str = Column(String)
    price = Column(Integer)
    name: str = Column(String(350))
    is_special: bool = Column(Boolean, default=False, nullable=False)
    is_vegan: bool = Column(Boolean, default=True, nullable=False)
    is_publish: bool = Column(Boolean, default=True, nullable=False)
    category_id = Column(Integer, ForeignKey("food_category.id"))

    category = relationship("FoodCategory", back_populates="foods")
    toppings = relationship(Topping, secondary='food_topping', back_populates="foods",
                            lazy="joined")  # , lazy="joined"

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls).options(joinedload(cls.toppings))  # для стягивания модели user при загрузке
        return (await session.scalars(query)).unique().all()

    @classmethod
    async def create(cls, session: AsyncSession, item: FoodCreate):
        food_create_arg = item.dict()
        if "toppings_id" in food_create_arg:
            toppings_id_list = food_create_arg.get("toppings_id")
            del food_create_arg["toppings_id"]
        new_post = cls(**food_create_arg)
        session.add(new_post)
        try:
            await session.commit()  # чтоб транзакция завершилась
            await session.refresh(new_post)
            return new_post
        except IntegrityError as ex:
            await session.rollback()
            raise DuplicatedEntryError(f"Category with id={new_post.category_id} not found")


foods = Food.__table__


class FoodCategory(Base, mixins.ModelMixin):
    __tablename__ = "food_category"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name: str = Column(String(350))
    is_publish: bool = Column(Boolean, default=True, nullable=False)

    foods = relationship("Food", back_populates="category", lazy="joined")  # selectin

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls).options(joinedload(cls.foods).joinedload(Food.toppings))
        return (await session.scalars(query)).unique().all()

    @classmethod
    async def get_by_filter(cls, filter_vegan, filter_special, filter_topping, session: AsyncSession):
        subq_food = select(Food.id).join(FoodTopping, isouter=True).join(Topping, isouter=True).filter(and_(Food.is_publish == True))
        if filter_vegan is not None:
            subq_food = subq_food.filter(and_(Food.is_vegan == filter_vegan))
        if filter_special is not None:
            subq_food = subq_food.filter(and_(Food.is_special == filter_special))
        if filter_topping != []:
            subq_food = subq_food.filter(and_(Food.toppings.and_(Topping.name.in_(filter_topping))))
        subq_food = subq_food.subquery()

        food_obj = cls.foods.and_(Food.id.in_(subq_food))

        query = select(cls).join(food_obj).join(Food.toppings, isouter=True).options(
            joinedload(food_obj).joinedload(Food.toppings))
        return (await session.scalars(query)).unique().all()

    @classmethod
    async def create(cls, session: AsyncSession, item: FoodCategoryCreate):
        new_post = cls(**item.dict())
        session.add(new_post)
        try:
            await session.commit()  # чтоб транзакция завершилась
            await session.refresh(new_post)
            return new_post
        except IntegrityError as ex:
            await session.rollback()
            raise DuplicatedEntryError("The post is already stored")


categoryes = FoodCategory.__table__


class FoodTopping(Base, mixins.ModelMixin):
    __tablename__ = "food_topping"

    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey('food.id'))
    topping_id = Column(Integer, ForeignKey('topping.id'))


foodstoppings = FoodTopping.__table__
