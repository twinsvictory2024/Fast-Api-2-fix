import os, datetime, uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from sqlalchemy import Integer, Float, String, DateTime, func, ForeignKey, UUID
from custom_types import ROLE

POSTGRES_DB = os.getenv( "POSTGRES_DB" )
POSTGRES_USER = os.getenv( "POSTGRES_USER" )
POSTGRES_PASSWORD = os.getenv( "POSTGRES_PASSWORD" )
POSTGRES_HOST = os.getenv( "POSTGRES_HOST" )
POSTGRES_PORT = os.getenv( "POSTGRES_PORT" )

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine( PG_DSN )

DbSession = async_sessionmaker( bind=engine, expire_on_commit=False )

class Base( DeclarativeBase, AsyncAttrs ):
    pass


    
class Users( Base ):
    __tablename__ = 'ads2_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    role: Mapped[ROLE] = mapped_column(String(20), nullable=False, default="user")
    tokens: Mapped[list["Token"]] = relationship( "Token", back_populates="user", cascade="all, delete-orphan", lazy="joined" )

    ads = relationship("AdsBase", back_populates="author")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }


class Token( Base ):
    __tablename__ = "ads2_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column( UUID, server_default=func.gen_random_uuid(), unique=True )
    creation_time: Mapped[datetime.datetime] = mapped_column( DateTime, server_default=func.now() )
    user_id: Mapped[int] = mapped_column( Integer, ForeignKey( Users.id ))
    user: Mapped[Users] = relationship( "Users", back_populates="tokens", lazy="joined" )


class AdsBase( Base ):
    __tablename__ = "ads2_table"

    id: Mapped[int] = mapped_column( Integer, primary_key=True, autoincrement=True )
    created_at: Mapped[datetime.datetime] = mapped_column( DateTime( timezone=True ), server_default=func.now() )
    title: Mapped[str] = mapped_column( String )
    description: Mapped[str] = mapped_column( String )
    price: Mapped[float] = mapped_column( Float )
    author_id: Mapped[int] = mapped_column( Integer, ForeignKey( Users.id ), nullable=False )

    author = relationship("Users", back_populates="ads")


    def dict(self):
        return { 
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author_id": self.author_id,
            }

async def init_orm():
    async with engine.begin() as conn:
        # await conn.run_sync( Base.metadata.drop_all ) 
        await conn.run_sync( Base.metadata.create_all )


async def close_orm():
    await engine.dispose()

ORM_OBJ = AdsBase | Users | Token
ORM_CLS = type[AdsBase] | type[Users] | type[Token]