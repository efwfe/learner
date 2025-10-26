"""
知识点管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...db.database import get_db
from ...schemas.knowledge import (
    KnowledgePointCreate,
    KnowledgePointUpdate,
    KnowledgePointResponse
)
from ...services.knowledge_service import KnowledgeService
from sqlalchemy import func

router = APIRouter()


@router.post("/", response_model=KnowledgePointResponse, status_code=201)
def create_knowledge_point(
    data: KnowledgePointCreate,
    generate_summary: bool = Query(True, description="是否自动生成摘要"),
    db: Session = Depends(get_db)
):
    """创建新的知识点"""
    service = KnowledgeService(db)
    return service.create_knowledge_point(data, generate_summary=generate_summary)


@router.get("/{kp_id}", response_model=KnowledgePointResponse)
def get_knowledge_point(kp_id: int, db: Session = Depends(get_db)):
    """获取指定知识点"""
    service = KnowledgeService(db)
    kp = service.get_knowledge_point(kp_id)
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return kp


@router.get("/", response_model=List[KnowledgePointResponse])
def list_knowledge_points(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    is_mastered: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """列出知识点"""
    service = KnowledgeService(db)
    return service.list_knowledge_points(
        category=category,
        tag=tag,
        is_mastered=is_mastered,
        skip=skip,
        limit=limit
    )


@router.put("/{kp_id}", response_model=KnowledgePointResponse)
def update_knowledge_point(
    kp_id: int,
    data: KnowledgePointUpdate,
    db: Session = Depends(get_db)
):
    """更新知识点"""
    service = KnowledgeService(db)
    kp = service.update_knowledge_point(kp_id, data)
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return kp


@router.delete("/{kp_id}", status_code=204)
def delete_knowledge_point(kp_id: int, db: Session = Depends(get_db)):
    """删除知识点"""
    service = KnowledgeService(db)
    if not service.delete_knowledge_point(kp_id):
        raise HTTPException(status_code=404, detail="知识点不存在")
    return None


@router.get("/stats/summary")
def get_knowledge_stats(db: Session = Depends(get_db)):
    """获取知识点统计信息"""
    from ...models.knowledge import KnowledgePoint
    
    total = db.query(KnowledgePoint).count()
    mastered = db.query(KnowledgePoint).filter(KnowledgePoint.is_mastered == True).count()
    
    # 按分类统计
    categories = {}
    results = db.query(
        KnowledgePoint.category, 
        db.query(func.count(KnowledgePoint.id)).scalar() # db.count(KnowledgePoint.id)
    ).group_by(KnowledgePoint.category).all()
    
    for category, count in results:
        categories[category or "未分类"] = count
    
    return {
        "total": total,
        "mastered": mastered,
        "in_progress": total - mastered,
        "mastery_rate": round(mastered / total * 100, 2) if total > 0 else 0,
        "by_category": categories
    }

