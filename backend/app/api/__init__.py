from fastapi import APIRouter
from .endpoints import knowledge, learning, review, graph

api_router = APIRouter()

# 注册各个端点
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(review.router, prefix="/review", tags=["review"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])

__all__ = ["api_router"]

