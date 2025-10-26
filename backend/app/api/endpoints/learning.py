"""
学习内容管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from ...db.database import get_db
from ...schemas.knowledge import (
    LearningContentCreate,
    LearningContentResponse
)
from ...services.knowledge_service import KnowledgeService
from ...models.knowledge import LearningContent

router = APIRouter()


@router.post("/", response_model=LearningContentResponse, status_code=201)
def create_learning_content(
    data: LearningContentCreate,
    auto_extract: bool = Query(True, description="是否自动提取知识点"),
    db: Session = Depends(get_db)
):
    """
    创建学习内容
    
    如果未指定 knowledge_point_id 且 auto_extract=True，
    系统会使用 GPT 自动提取知识点
    """
    service = KnowledgeService(db)
    return service.create_learning_content(data, auto_extract_knowledge=auto_extract)


@router.get("/", response_model=List[LearningContentResponse])
def list_learning_contents(
    knowledge_point_id: int = None,
    days: int = Query(7, description="查询最近几天的学习内容"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """列出学习内容"""
    query = db.query(LearningContent)
    
    if knowledge_point_id:
        query = query.filter(LearningContent.knowledge_point_id == knowledge_point_id)
    
    # 按日期过滤
    start_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(LearningContent.learning_date >= start_date)
    
    return query.order_by(
        LearningContent.learning_date.desc()
    ).offset(skip).limit(limit).all()


@router.get("/stats/daily")
def get_daily_learning_stats(
    days: int = Query(30, description="统计最近几天"),
    db: Session = Depends(get_db)
):
    """获取每日学习统计"""
    from sqlalchemy import func
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        func.date(LearningContent.learning_date).label('date'),
        func.count(LearningContent.id).label('count')
    ).filter(
        LearningContent.learning_date >= start_date
    ).group_by(
        func.date(LearningContent.learning_date)
    ).all()
    
    stats = {
        str(result.date): result.count
        for result in results
    }
    
    return {
        "period_days": days,
        "total_items": sum(stats.values()),
        "daily_stats": stats
    }

