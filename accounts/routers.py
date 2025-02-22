from ninja import Router
from django.contrib.auth import aauthenticate, get_user_model
from accounts.schemas import UserRegister, UserSchema, UserUpdateSchema
from accounts.utils import create_access_token, create_refresh_token
from accounts.auth import RefreshTokenObtain, RefreshTokenDelete, AuthBearer

accounts_router = Router()


@accounts_router.post("/register/", response=UserSchema)
async def create_user(request, data: UserRegister):
    user = get_user_model()(email=data.email, username=data.email)
    user.set_password(data.password)
    await user.asave()
    return user


@accounts_router.post("/login/")
async def login(request, data: UserRegister):
    user = await aauthenticate(request=request, username=data.email, password=data.password)
    if not user:
        return {"message": "Invalid data"}
    access_token = await create_access_token(user.id)
    refresh_token = await create_refresh_token(user.id)
    return {
        'access': access_token,
        'refresh': refresh_token.token
    }


@accounts_router.post("/refresh/", auth=RefreshTokenObtain())
async def refresh(request):
    return {
        'refresh_token': request.auth
    }


@accounts_router.post("/logout/", auth=RefreshTokenDelete())
async def logout(request):
    return {
        "success": "User logged out."
    }


@accounts_router.get("/me/", auth=AuthBearer(), response=UserSchema)
async def get_user(request):
    return await get_user_model().objects.aget(id=request.auth)


@accounts_router.put("/me/", auth=AuthBearer(), response=UserSchema)
async def update_user(request, data: UserUpdateSchema):
    await get_user_model().objects.filter(id=request.auth).aupdate(**data.dict(exclude_unset=True))
    return await get_user_model().objects.aget(id=request.auth)