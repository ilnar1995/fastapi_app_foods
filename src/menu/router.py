from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.core.db import get_db_session
from .schemas import FoodCategoryList, FoodCategoryCreate, FoodList, FoodCreate, ToppingCreate, ToppingGetOne
from .models import Food, FoodCategory, Topping

router = APIRouter()


@router.get('/category', response_model=List[FoodCategoryList])
async def category_list(db: AsyncSession = Depends(get_db_session)):
    return await FoodCategory.get_all(db)


@router.get('/public_food_by_filter', response_model=List[FoodCategoryList])
async def category_list(filter_vegan: bool = Query(default=None), filter_special: bool = Query(default=None),
                        filter_topping: list = Query(default=[]),
                        db: AsyncSession = Depends(get_db_session)):
    return await FoodCategory.get_by_filter(filter_vegan, filter_special, filter_topping, db)


@router.post('/category', response_model=FoodCategoryList)
async def create_category(item: FoodCategoryCreate, db: AsyncSession = Depends(get_db_session)):
    posts = await FoodCategory.create(db, item)
    return posts


@router.get('/food', response_model=List[FoodList])
async def category_food_list(db: AsyncSession = Depends(get_db_session)):
    return await Food.get_all(db)


@router.post('/food', response_model=FoodList)
async def create_food(item: FoodCreate, db: AsyncSession = Depends(get_db_session)):
    posts = await Food.create(db, item)
    return posts


@router.get('/topping', response_model=List[ToppingGetOne])
async def topping_list(db: AsyncSession = Depends(get_db_session)):
    return await Topping.get_all(db)


@router.post('/topping', response_model=ToppingGetOne)
async def create_topping(item: ToppingCreate, db: AsyncSession = Depends(get_db_session)):
    posts = await Topping.create(db, item)
    return posts
