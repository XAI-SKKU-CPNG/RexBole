from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# Enums
class InteractionType(int, Enum):
    VIEW = 0
    ADD_TO_CART = 1
    PURCHASE = 2


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(sa_column_kwargs={"unique": True, "index": True})
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: Optional[str] = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: Optional[str] = None  # type: ignore
    password: Optional[str] = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    interactions: List["Interaction"] = Relationship(back_populates="user")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: List[UserOut]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: Optional[str] = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    interactions: List["Interaction"] = Relationship(back_populates="item")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int


class ItemsOut(SQLModel):
    data: List[ItemOut]
    count: int

class ExplainationOut(SQLModel):
    item_id: int
    interaction_type: InteractionType
    item_name: str

class RecommendationOut(SQLModel):
    rec_item_id: int
    rec_item_name: str
    explanations: List[ExplainationOut]

class RecommendationsOut(SQLModel):
    data: List[RecommendationOut]
    count: int


# Interaction model to link User and Item
class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    count: int
    interaction_type: InteractionType
    item_id: int = Field(foreign_key="item.id")
    user_id: int = Field(foreign_key="user.id")
    item: Item = Relationship(back_populates="interactions")
    user: User = Relationship(back_populates="interactions")


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: Optional[int] = None


class NewPassword(SQLModel):
    token: str
    new_password: str
