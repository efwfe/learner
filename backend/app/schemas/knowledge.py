from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# 知识点 Schemas
class KnowledgePointBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: Optional[str] = None
    tags: Optional[str] = None


class KnowledgePointCreate(KnowledgePointBase):
    pass


class KnowledgePointUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_mastered: Optional[bool] = None


class KnowledgePointResponse(KnowledgePointBase):
    id: int
    summary: Optional[str]
    ease_factor: float
    interval: int
    repetitions: int
    next_review_date: datetime
    created_at: datetime
    updated_at: datetime
    is_mastered: bool
    
    class Config:
        from_attributes = True


# 学习内容 Schemas
class LearningContentBase(BaseModel):
    content: str = Field(..., min_length=1)
    source: Optional[str] = None
    notes: Optional[str] = None


class LearningContentCreate(LearningContentBase):
    knowledge_point_id: Optional[int] = None  # 可选，如果为空则创建新知识点


class LearningContentResponse(LearningContentBase):
    id: int
    knowledge_point_id: int
    learning_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# 复习记录 Schemas
class ReviewRecordCreate(BaseModel):
    knowledge_point_id: int
    quality: int = Field(..., ge=0, le=5)
    time_spent_seconds: Optional[int] = None
    notes: Optional[str] = None


class ReviewRecordResponse(ReviewRecordCreate):
    id: int
    ease_factor_before: Optional[float]
    interval_before: Optional[int]
    ease_factor_after: Optional[float]
    interval_after: Optional[int]
    reviewed_at: datetime
    
    class Config:
        from_attributes = True


# 知识关系 Schemas
class KnowledgeRelationCreate(BaseModel):
    parent_id: int
    child_id: int
    relation_type: str = "related"
    strength: float = Field(1.0, ge=0.0, le=1.0)
    description: Optional[str] = None


class KnowledgeRelationResponse(KnowledgeRelationCreate):
    id: int
    created_at: datetime
    created_by_ai: bool
    
    class Config:
        from_attributes = True


# 每日复习计划
class DailyReviewPlan(BaseModel):
    date: datetime
    total_reviews: int
    reviews_by_priority: dict[str, List[KnowledgePointResponse]]  # high, medium, low
    estimated_time_minutes: int


# 知识图谱相关
class KnowledgeGraphNode(BaseModel):
    id: int
    title: str
    category: Optional[str]
    is_mastered: bool
    ease_factor: float
    repetitions: int


class KnowledgeGraphEdge(BaseModel):
    source: int
    target: int
    relation_type: str
    strength: float


class KnowledgeGraph(BaseModel):
    nodes: List[KnowledgeGraphNode]
    edges: List[KnowledgeGraphEdge]

