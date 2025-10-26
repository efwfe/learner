"""
Learner - 智能学习管理系统
基于遗忘曲线的个人知识管理平台
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .core.config import settings
from .db.database import engine, Base
from .api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时：清理资源（如果需要）


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    基于遗忘曲线的智能学习管理系统
    
    ## 功能特性
    
    * **学习内容管理** - 记录每日学习内容，自动提取知识点
    * **智能复习** - 基于 SuperMemo SM-2 算法的间隔重复系统
    * **知识图谱** - 构建知识点之间的关联，形成知识体系
    * **AI 辅助** - 使用 Azure OpenAI 自动生成摘要、建议关系
    
    ## 核心概念
    
    * **知识点 (Knowledge Point)** - 独立的知识单元
    * **学习内容 (Learning Content)** - 每日学习记录
    * **复习记录 (Review Record)** - 复习历史和质量评分
    * **知识关系 (Knowledge Relation)** - 知识点间的关联
    """,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to Learner API",
        "version": settings.VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    from .services.openai_service import openai_service
    
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "openai_available": openai_service.is_available()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

