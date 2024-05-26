from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi_versioning import version
from app.orders.dao import OrderDAO
from app.orders.shemas import SOrder, SOrderCrate, SOrderUpdate
from app.orders.models import OrderStatus

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)


@router.get("")
async def get_orders() -> List[SOrder]:
    return await OrderDAO.find_all()


@router.get("/{status}")
@version(2)
async def get_orders_by_status(status: OrderStatus) -> List[SOrder]:
    return await OrderDAO.find_all(status=status)


@router.post("")
async def create_order(data: SOrderCrate = Depends()) -> SOrder:
    try:
        new_order = await OrderDAO.create(user_id=data.user_id, product_id=data.product_id)
        return new_order
    except:
        raise HTTPException(501, detail="Order not create. Check the parameters ")


@router.delete("/{order_id}")
async def delete(order_id: int) -> SOrder:
    try:
        result = await OrderDAO.delete(id=order_id)
        return result
    except:
        raise HTTPException(501, detail="Order not delete. Check the product id ")


@router.patch("/status/{order_id}")
async def update_status(order_data: SOrderUpdate = Depends()) -> SOrder:
    product = await OrderDAO.find_by_id(order_data.id)
    if not product:
        raise HTTPException(status_code=404, detail="Order not found")
    update_data = order_data.dict(exclude_none=True)
    try:
        updated_prodcut = await OrderDAO.update(filter_by={"id": order_data.id}, **update_data)
        return updated_prodcut
    except:
        raise HTTPException(500, detail="Failed to update order status ")
