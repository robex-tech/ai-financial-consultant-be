from api.routers.auth import router as auth_router
from api.routers.users import router as users_router
from api.routers.dialogs import router as dialog_router


all_routes = [
    auth_router,
    users_router,
    dialog_router
]
