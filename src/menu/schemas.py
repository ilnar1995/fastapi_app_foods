from typing import List

from pydantic import BaseModel, validator
from datetime import datetime
from pydantic.datetime_parse import parse_datetime
from sqlalchemy.orm import Relationship


class ToppingBase(BaseModel):
    name: str = None


class ToppingCreate(ToppingBase):
    pass


class ToppingList(ToppingBase):
    pass

    class Config:
        orm_mode = True

class ToppingGetOne(ToppingList):
    id: int

class FoodBase(BaseModel):
    description: str
    price: int
    name: str
    is_special: bool
    is_vegan: bool
    is_publish: bool


class FoodList(FoodBase):
    id: int
    toppings: List[str] = []

    class Config:
        orm_mode = True

    @validator("toppings", pre=True)
    def toppings_validate(cls, date):
        return [topping.name for topping in date]

class FoodCreate(FoodBase):
    category_id: int
    toppings_id: List[int] = None

    class Config:
        orm_mode = True


class FoodCategoryBase(BaseModel):
    name: str
    is_publish: bool


class FoodCategoryList(FoodCategoryBase):
    id: int
    foods: List[FoodList] = None
    # cats: List[str] = None

    class Config:
        orm_mode = True


class FoodCategoryCreate(FoodCategoryBase):
    class Config:
        orm_mode = True

