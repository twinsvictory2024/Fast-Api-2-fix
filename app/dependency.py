import os, datetime, uuid

from typing import Annotated
from models import DbSession, Token
from fastapi import Depends, HTTPException, Header


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncSession:
    async with DbSession() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]

TOKEN_TTL_SEC = int(os.getenv('TOKEN_TTL_SEC', 172800))


async def get_token( x_token: Annotated[uuid.UUID, Header()], session: SessionDependency ) -> Token:
    if x_token is None:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    query = select(Token).where(
        Token.token == x_token,
        Token.creation_time >= datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC)
    )
    token = await session.scalar(query)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

TokenDependency = Annotated[Token, Depends(get_token, use_cache=True)]

