from api.endpoints.auth import router as auth_router
from api.endpoints.users import router as users_router
from api.endpoints.dialogs import router as dialog_router


all_routes = [
    auth_router,
    users_router,
    dialog_router
]
