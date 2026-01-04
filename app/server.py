from fastapi import FastAPI

from lifespan import lifespan
from dependency import SessionDependency, TokenDependency

from schema import AdCreate, AdResponse, AdUpdate, CreateUserRequest, CreateUserResponce, LoginRequest, LoginResponce
from schema import GetUserResponce, UpdateUserRequest, UpdateUserResponce
from models import AdsBase, Users, Token


from auth import verify_password, hash_password
import crud

app = FastAPI(
    title="FastAPI_Homework_2",
    description="Part 2 of FastAPI homework",
    lifespan=lifespan
)


@app.post("/user/", tags=["sign_up"], response_model=CreateUserResponce)
async def create_user_endpoint(  session: SessionDependency, user_input: CreateUserRequest ):
    user_obj = Users(
        name = user_input.name,
        password = hash_password( user_input.password )
    )
    return await crud.create_user( session, user_obj )


@app.patch("/user/{user_id}", tags=["users"], response_model=UpdateUserResponce)
async def update_user_endpoint( session: SessionDependency, user_id: int, input_userdata: UpdateUserRequest, token: TokenDependency ):
    update_userdata = input_userdata.model_dump(exclude_unset=True)
    return await crud.update_user(session, Users, token, user_id, update_userdata)

@app.delete("/user/{user_id}", tags=["users"])
async def delete_user_endpoint( session: SessionDependency, user_id: int, token: TokenDependency ):
    return await crud.delete_user(session, Users, token, user_id)



@app.post("/login/", tags=["login"], response_model=LoginResponce)
async def login_endpoint(session: SessionDependency, login_data: LoginRequest ):
    token = await crud.login_user(session, Users, Token, login_data )
    return token


@app.get("/user/{user_id}", tags=["users"], response_model=GetUserResponce)
async def get_user_endpoint(session: SessionDependency, user_id: int ):
    return await crud.get_user_by_id(session, Users, user_id)







@app.post('/advertisement', tags=["advertisements"], response_model=AdResponse)
async def create_adv_endpoint( session: SessionDependency, ad_item: AdCreate, token: TokenDependency ):
    ad = AdsBase(
        title = ad_item.title,
        description = ad_item.description,
        price = ad_item.price,
        author_id = token.user_id,
    )
    resp_ad = await crud.create_ad( session, token, ad )
    return resp_ad

@app.get('/advertisement/{ad_id}', tags=["advertisements"], response_model=AdResponse)
async def get_ad_endpoint( session: SessionDependency, ad_id: int ):
    ad = await crud.get_ad_by_id( session, AdsBase, ad_id )
    return ad


@app.get('/advertisement/', tags=["advertisements"], response_model= list[ AdResponse ] )
async def search_adv_endpoint( session: SessionDependency, 
                    title:  str | None = None,
                    description:  str | None = None,
                    author_id: int | None = None,
                    price:  float | None = None,
                    limit: int = 100,
                    offset: int = 0
                    ):
    search_params = {}
    if title:
        search_params["title"] = title
    if description:
        search_params["description"] = description
    if author_id:
        search_params["author_id"] = author_id
    if price:
        search_params["price"] = price
    if limit:
        search_params["limit"] = limit
    if offset:
        search_params["offset"] = offset


    ads = await crud.search_ad( session, AdsBase, search_params )
    return ads

@app.patch('/advertisement/{ad_id}', tags=["advertisements"], response_model=AdResponse)
async def update_adv_endpoint( session: SessionDependency, ad_id: int, update_item: AdUpdate, token: TokenDependency):
    ad = await crud.update_ad( session, AdsBase, token, ad_id, update_item )
    return ad

@app.delete('/advertisement/{ad_id}', tags=["advertisements"])
async def delete_adv_endpoint( session: SessionDependency, ad_id: int, token: TokenDependency ):
    msg = await crud.delete_ad( session, AdsBase, token, ad_id )
    return msg
