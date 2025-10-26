"""
复习管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...db.database import get_db
from ...schemas.knowledge import (
    ReviewRecordCreate,
    ReviewRecordResponse,
    DailyReviewPlan,
    KnowledgePointResponse
)
from ...services.knowledge_service import KnowledgeService
from ...services.openai_service import openai_service
from ...models.knowledge import ReviewRecord

router = APIRouter()


@router.post("/", response_model=ReviewRecordResponse, status_code=201)
def create_review_record(
    data: ReviewRecordCreate,
    db: Session = Depends(get_db)
):
    """
    创建复习记录
    
    quality 评分标准：
    - 0: 完全不记得
    - 1: 错误答案
    - 2: 错误但想起来了
    - 3: 困难但正确
    - 4: 犹豫后正确
    - 5: 完美记忆
    """
    service = KnowledgeService(db)
    try:
        return service.create_review_record(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/plan", response_model=dict)
def get_review_plan(
    date: datetime = Query(None, description="指定日期，默认为今天"),
    db: Session = Depends(get_db)
):
    """获取复习计划"""
    service = KnowledgeService(db)
    plan = service.get_daily_review_plan(date)
    
    # 将知识点对象转换为响应模型
    result = {
        "date": plan["date"],
        "total_reviews": plan["total_reviews"],
        "estimated_time_minutes": plan["estimated_time_minutes"],
        "reviews_by_priority": {}
    }
    
    for priority, kps in plan["reviews_by_priority"].items():
        result["reviews_by_priority"][priority] = [
            KnowledgePointResponse.model_validate(kp) for kp in kps
        ]
    
    return result


@router.get("/due", response_model=List[KnowledgePointResponse])
def get_due_reviews(
    limit: int = Query(10, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """获取待复习的知识点（按优先级排序）"""
    from ...models.knowledge import KnowledgePoint
    from sqlalchemy import and_
    
    # 查询需要复习的知识点
    knowledge_points = db.query(KnowledgePoint).filter(
        and_(
            KnowledgePoint.is_mastered == False,
            KnowledgePoint.next_review_date <= datetime.utcnow()
        )
    ).order_by(
        KnowledgePoint.next_review_date.asc(),
        KnowledgePoint.ease_factor.asc()
    ).limit(limit).all()
    
    return knowledge_points


@router.get("/question/{kp_id}")
async def generate_review_question(
    kp_id: int,
    db: Session = Depends(get_db)
):
    """为指定知识点生成复习问题"""
    service = KnowledgeService(db)
    kp = service.get_knowledge_point(kp_id)
    
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")
    
    question = await openai_service.generate_review_question({
        "title": kp.title,
        "content": kp.content,
        "summary": kp.summary
    })
    
    return {
        "knowledge_point_id": kp_id,
        "question": question,
        "knowledge_point": KnowledgePointResponse.model_validate(kp)
    }


@router.get("/history/{kp_id}", response_model=List[ReviewRecordResponse])
def get_review_history(
    kp_id: int,
    limit: int = Query(50, description="返回记录数量"),
    db: Session = Depends(get_db)
):
    """获取知识点的复习历史"""
    records = db.query(ReviewRecord).filter(
        ReviewRecord.knowledge_point_id == kp_id
    ).order_by(
        ReviewRecord.reviewed_at.desc()
    ).limit(limit).all()
    
    return records


@router.get("/stats/overall")
def get_review_stats(db: Session = Depends(get_db)):
    """获取复习统计信息"""
    from ...models.knowledge import KnowledgePoint
    from sqlalchemy import func, and_
    
    # 待复习数量
    due_count = db.query(KnowledgePoint).filter(
        and_(
            KnowledgePoint.is_mastered == False,
            KnowledgePoint.next_review_date <= datetime.utcnow()
        )
    ).count()
    
    # 今日已复习数量
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    reviewed_today = db.query(ReviewRecord).filter(
        ReviewRecord.reviewed_at >= today_start
    ).count()
    
    # 平均复习质量
    avg_quality = db.query(func.avg(ReviewRecord.quality)).scalar() or 0
    
    return {
        "due_reviews": due_count,
        "reviewed_today": reviewed_today,
        "average_quality": round(avg_quality, 2)
    }

