from pydantic import BaseModel, Field

import datetime, uuid
from custom_types import ROLE

class AdCreate( BaseModel ):
    title: str
    description: str
    price: float = Field( gt=0 )
    author_id: int



class AdResponse( BaseModel ):
    id: int
    created_at: datetime.datetime
    title: str
    description: str
    price: float
    author_id: int


class AdUpdate( BaseModel ):
    title: str | None = None
    description: str | None = None
    price: float | None = Field( gt=0, default=None )

class BaseUserRequest( BaseModel ):
    name: str
    password: str

class LoginRequest( BaseUserRequest ):
    name: str
    password: str

class LoginResponce( BaseModel ):
    token: uuid.UUID

class CreateUserRequest ( BaseUserRequest ):
    name: str
    password: str

class CreateUserResponce ( BaseModel ):
    id: int

    
class GetUserResponce ( BaseModel ):
    id: int
    name: str
    role: ROLE


class UpdateUserRequest ( BaseModel ):
    name: str | None = None
    password: str | None = None
    role: ROLE | None = None

class UpdateUserResponce ( BaseModel ):
    id: int
    name: str
    role: ROLE