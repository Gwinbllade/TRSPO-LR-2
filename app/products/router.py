from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi_versioning import version


from app.products.dao import ProductDAO
from app.products.shemas import SAddProduct, SProduct, SUpdateProduct

router = APIRouter(
    prefix="/products",
    tags=['Products']
)



@router.get("")
@version(1)
async def get_products() -> List[SProduct]:
    products = await ProductDAO.find_all()
    return products


@router.get("")
@version(2)
async def get_products(category_id: Optional[int] = None) -> List[SProduct]:
    if category_id is not None:
        products = await ProductDAO.find_all(category_id=category_id)
    else:
        products = await ProductDAO.find_all()
    return products


@router.post("")
async def add_product(args: SAddProduct = Depends()) -> SProduct:
    try:
        result = await ProductDAO.add(name=args.name, cost=args.cost, category_id=args.category_id)
        return result
    except:
        raise HTTPException(501, detail="product not added. Check the parameters ")


@router.delete("/{product_id}")
async def delete_product(product_id: int) -> SProduct:
    try:
        result = await ProductDAO.delete(id=product_id)
        return result
    except:
        raise HTTPException(501, detail="product not delete. Check the product id ")

@router.patch("")
async def update(product_data: SUpdateProduct = Depends()) -> SProduct:
    product = await ProductDAO.find_by_id(product_data.id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.dict(exclude_none=True)
    updated_product = await ProductDAO.update(filter_by={"id": product_data.id}, **update_data)

    if updated_product is not None:
        return updated_product
    else:
        raise HTTPException(status_code=500, detail="Failed to update product")
