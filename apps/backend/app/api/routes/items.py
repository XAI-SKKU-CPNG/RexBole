from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, delete

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemOut, ItemsOut, ItemUpdate, Message, Interaction, InteractionType

router = APIRouter()


@router.get("/", response_model=ItemsOut)
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    statement = select(func.count()).select_from(Item)
    count = session.exec(statement).one()
    statement = select(Item).offset(skip).limit(limit)
    items = session.exec(statement).all()

    return ItemsOut(data=items, count=count)


@router.get("/{id}", response_model=ItemOut)
def read_item(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get item by ID.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return item


@router.post("/", response_model=ItemOut)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    item = Item.model_validate(item_in)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.put("/{id}", response_model=ItemOut)
def update_item(
    *, session: SessionDep, current_user: CurrentUser, id: int, item_in: ItemUpdate
) -> Any:
    """
    Update an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{id}")
def delete_item(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not current_user.is_superuser :
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")
