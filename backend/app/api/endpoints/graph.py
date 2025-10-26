"""
知识图谱 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...db.database import get_db
from ...schemas.knowledge import (
    KnowledgeRelationCreate,
    KnowledgeRelationResponse,
    KnowledgeGraph
)
from ...services.knowledge_service import KnowledgeService

router = APIRouter()


@router.post("/relations", response_model=KnowledgeRelationResponse, status_code=201)
def create_knowledge_relation(
    data: KnowledgeRelationCreate,
    db: Session = Depends(get_db)
):
    """创建知识点之间的关系"""
    service = KnowledgeService(db)
    return service.create_knowledge_relation(data)


@router.get("/", response_model=KnowledgeGraph)
def get_knowledge_graph(
    center_id: Optional[int] = Query(None, description="中心节点ID，为空则返回全局图谱"),
    depth: int = Query(2, description="图谱深度", ge=1, le=5),
    db: Session = Depends(get_db)
):
    """获取知识图谱"""
    service = KnowledgeService(db)
    graph_data = service.get_knowledge_graph(center_id=center_id, depth=depth)
    return graph_data


@router.get("/suggest/{kp_id}")
def suggest_relations(
    kp_id: int,
    max_suggestions: int = Query(5, description="最大建议数量", ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    使用 AI 自动建议知识关系
    
    系统会分析指定知识点与其他知识点的关联，
    并建议可能的关系类型和强度
    """
    service = KnowledgeService(db)
    suggestions = service.auto_suggest_relations(kp_id, max_suggestions=max_suggestions)
    
    return {
        "knowledge_point_id": kp_id,
        "suggestions": suggestions
    }


@router.post("/batch-relations", status_code=201)
def create_batch_relations(
    relations: List[KnowledgeRelationCreate],
    db: Session = Depends(get_db)
):
    """批量创建知识关系"""
    service = KnowledgeService(db)
    created = []
    
    for relation_data in relations:
        try:
            relation = service.create_knowledge_relation(relation_data, created_by_ai=True)
            created.append(relation)
        except Exception as e:
            # 跳过错误的关系，继续处理其他
            continue
    
    return {
        "created_count": len(created),
        "relations": created
    }


@router.get("/categories")
def get_knowledge_categories(db: Session = Depends(get_db)):
    """获取所有知识分类及其统计"""
    from ...models.knowledge import KnowledgePoint
    from sqlalchemy import func
    
    results = db.query(
        KnowledgePoint.category,
        func.count(KnowledgePoint.id).label('count'),
        func.avg(KnowledgePoint.ease_factor).label('avg_ease_factor'),
        func.sum(KnowledgePoint.is_mastered).label('mastered_count')
    ).group_by(KnowledgePoint.category).all()
    
    categories = []
    for result in results:
        categories.append({
            "name": result.category or "未分类",
            "count": result.count,
            "average_ease_factor": round(result.avg_ease_factor or 0, 2),
            "mastered_count": result.mastered_count or 0,
            "mastery_rate": round((result.mastered_count or 0) / result.count * 100, 2)
        })
    
    return {"categories": categories}

