from fastapi import APIRouter

from src.routers.v1.endpoints import todo_list

router_list = (todo_list.router,)

router = APIRouter()

for r in router_list:
    r.tags.append("v1")
    router.include_router(r)
