from models import ORM_CLS, ORM_OBJ

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

from auth import hash_password, verify_password
from custom_types import ROLE


async def create_token( session: AsyncSession, orm_cls: ORM_CLS, user_id: int ) -> ORM_OBJ:
    token = orm_cls(user_id=user_id)
    session.add(token)
    await session.commit()
    return token


async def create_user( session: AsyncSession, user: ORM_OBJ ) -> ORM_OBJ:
    try:
        session.add(user)
        await session.commit()
        return user
    except IntegrityError:
        raise HTTPException( 409, "User already exists" )

async def get_user_by_id( session: AsyncSession, orm_cls: ORM_CLS, user_id: int ) -> ORM_OBJ:
    user = await session.get( orm_cls, user_id )
    if not user:
        raise HTTPException( 404, "User not found" )
    return user


async def get_user_by_username( session: AsyncSession, orm_cls: ORM_CLS, username: str ) -> ORM_OBJ:
    query = select(orm_cls).filter(orm_cls.name == username)
    user = await session.execute(query)
    user = user.scalars().first()
    if not user:
        raise HTTPException( 401, "Invalid credentials")
    return user



async def login_user( session: AsyncSession, orm_users: ORM_CLS, orm_tokens: ORM_CLS, login_data: dict ) -> ORM_OBJ:
    try:
        user = await get_user_by_username( session, orm_users, login_data.name )
        if not verify_password(login_data.password, user.password):
            raise HTTPException( 401, "Invalid credentials" )
        
        return await create_token(session, orm_tokens, user.id)
    except IntegrityError:
        raise HTTPException( 409, "User already exists" )


async def update_user( db_session: AsyncSession, orm_cls: ORM_CLS, token: ORM_OBJ, user_id: int, user_data: dict ) -> ORM_OBJ:
    user = await db_session.get(orm_cls, user_id)


    if not user:
        raise HTTPException( 404, "User not found" )
    
    # Проверка на админа или самого пользователя
    if token.user.role == "admin" or token.user.id == user.id:
        
        for key, value in user_data.items():
            # Роль меняется только от админа, проверка на корректную роль
            if key == 'role' and token.user.role != "admin":
                if value not in ["user", "admin"]:
                    raise HTTPException( 422, "Invalid role")
                continue
            
            # Хешируем новый пароль
            if key == 'password':
                value = hash_password(value)

            # заменяем значения полей
            if value is not None:
                setattr( user, key, value )
        
        try:
            await db_session.commit()
            return user
        except IntegrityError:
            raise HTTPException( 409, "Update failed")
    
    else:
        raise HTTPException( 403, "Insufficient permissions" )
    
    

async def delete_user( session: AsyncSession, orm_cls: ORM_CLS, token: ORM_OBJ, user_id: int ) -> ORM_OBJ:
    user = await session.get( orm_cls, user_id )
    if not user:
        raise HTTPException( 404, "User not found" )

    if token.user.role == "admin" or token.user.id == user.id:
        await session.delete( user )
        await session.commit()
        return {"deleted_user_id": user_id}
    
    raise HTTPException( 403, "Insufficient permissions" )
    

async def get_ad_by_id( session: AsyncSession, orm_cls: ORM_CLS, ad_id: int ) -> ORM_OBJ:
    orm_obj = await session.get( orm_cls, ad_id )
    if orm_obj is None:
        raise HTTPException( 404, "Advertisement not found" )
    return orm_obj

async def search_ad( session: AsyncSession, orm_cls: ORM_CLS, queryparams: dict | None = None) -> list[ORM_OBJ]:
    query = select(orm_cls)
    limit: int = 100
    offset: int = 0

    if queryparams:
        conditions = []
        if "title" in queryparams:
            conditions.append( orm_cls.title.ilike( f"%{ queryparams['title'] }" ) )
        if "description" in queryparams:
            conditions.append( orm_cls.description.ilike( f"%{ queryparams['description'] }" ) )
        if "author_id" in queryparams:
            conditions.append( orm_cls.author_id == queryparams['author_id'] )
        if "price" in queryparams:
            conditions.append( orm_cls.price == queryparams['price'] )
        if "limit" in queryparams:
            limit = queryparams['limit']
        if "offset" in queryparams:
            limit = queryparams['offset']

        if conditions:
            query = query.where( and_( *conditions ) ).limit(limit).offset(offset)

    result = await session.execute(query)
    return result.scalars().all()

async def create_ad( session: AsyncSession, token: ORM_OBJ, ad_item: ORM_OBJ ):
    try:
        session.add( ad_item )
        await session.commit()
        return ad_item
    except IntegrityError:
        raise HTTPException( 409, "Advertisement already exist" )

async def update_ad( session: AsyncSession, orm_cls: ORM_CLS, token: ORM_OBJ, ad_id: int, updated_item: dict ):
    ad = await session.get( orm_cls, ad_id )
    
    if not ad:
        raise HTTPException( 404, "Advertisement not found" )
    
    if token.user.id == ad.author_id or token.user.role == "admin":
        

        for key, value in updated_item:
            if value is not None:
                setattr( ad, key, value )
    
        await session.commit()
        return ad
    raise HTTPException( 403, "Insufficient permissions" )



async def delete_ad( session: AsyncSession, orm_cls: ORM_CLS, token: ORM_OBJ, ad_id: int):
    ad = await session.get( orm_cls, ad_id )

    if not ad:
        raise HTTPException( 404, "Advertisement not found" )
    
    if token.user.id == ad.author_id or token.user.role == "admin" :
    
        await session.delete(ad)
        await session.commit()
        return {"deleted_id": ad_id}
    raise HTTPException( 403, "Insufficient permissions" )


