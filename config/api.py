from ninja import NinjaAPI
from accounts.routers import accounts_router

api = NinjaAPI()

api.add_router("/account/", accounts_router)


