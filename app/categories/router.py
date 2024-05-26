from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi_versioning import version

from app.categories.dao import CategoriaDAO
from app.categories.shemas import SCategory, SAddCategory, SUpdateCategories

router = APIRouter(
    prefix="/categories",
    tags=['Categories']
)


@router.get("")
async def get_categories() -> List[SCategory]:
    categories = await CategoriaDAO.find_all()
    return categories


@router.get("/{category_id}")
@version(2)
async def get_category(category_id: int) -> SCategory:
    categories = await CategoriaDAO.find_one_or_none(id=category_id)
    if categories is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories


@router.post("")
async def add(args: SAddCategory = Depends()) -> SCategory:
    try:
        new_categories = await CategoriaDAO.add(name=args.name)
        return new_categories
    except:
        raise HTTPException(501, detail="Category not added. Check the parameters ")


@router.delete("/{category_id}")
async def delete(category_id: int) -> SCategory:
    try:
        result = await CategoriaDAO.delete(id=category_id)
        return result
    except:
        raise HTTPException(501, detail="Category not delete. Check the product id ")



@router.put("/{category_id}")
async def update(category_id: int, category_data: SUpdateCategories = Depends()) -> SCategory:
    category = await CategoriaDAO.find_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category_data.dict(exclude_none=True)
    try:
        updated_count = await CategoriaDAO.update(filter_by={"id": category_id}, **update_data)
        return updated_count
    except:
        raise HTTPException(status_code=500, detail="Failed to update category")

