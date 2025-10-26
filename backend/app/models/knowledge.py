from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base


class KnowledgePoint(Base):
    """知识点模型 - 核心知识点存储"""
    __tablename__ = "knowledge_points"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)  # GPT生成的摘要
    category = Column(String(100), index=True)  # 分类
    tags = Column(String(500))  # 标签，逗号分隔
    
    # 遗忘曲线相关字段
    ease_factor = Column(Float, default=2.5)  # 难易度因子（SM-2算法）
    interval = Column(Integer, default=0)  # 复习间隔（天）
    repetitions = Column(Integer, default=0)  # 重复次数
    next_review_date = Column(DateTime, default=datetime.utcnow)  # 下次复习时间
    
    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_mastered = Column(Boolean, default=False)  # 是否已掌握
    
    # 关系
    learning_contents = relationship("LearningContent", back_populates="knowledge_point")
    review_records = relationship("ReviewRecord", back_populates="knowledge_point")
    parent_relations = relationship(
        "KnowledgeRelation",
        foreign_keys="KnowledgeRelation.child_id",
        back_populates="child"
    )
    child_relations = relationship(
        "KnowledgeRelation",
        foreign_keys="KnowledgeRelation.parent_id",
        back_populates="parent"
    )


class LearningContent(Base):
    """学习内容模型 - 每日学习记录"""
    __tablename__ = "learning_contents"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"))
    content = Column(Text, nullable=False)  # 原始学习内容
    source = Column(String(200))  # 来源（书籍、课程等）
    notes = Column(Text)  # 笔记
    
    # 元数据
    learning_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    knowledge_point = relationship("KnowledgePoint", back_populates="learning_contents")


class ReviewRecord(Base):
    """复习记录模型 - 记录每次复习情况"""
    __tablename__ = "review_records"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    
    # 复习质量评分（SM-2算法）
    # 0: 完全不记得, 1: 错误答案, 2: 错误但想起来了, 3: 困难但正确, 4: 犹豫后正确, 5: 完美记忆
    quality = Column(Integer, nullable=False)
    
    # 复习时的数据快照
    ease_factor_before = Column(Float)
    interval_before = Column(Integer)
    ease_factor_after = Column(Float)
    interval_after = Column(Integer)
    
    # 元数据
    reviewed_at = Column(DateTime, default=datetime.utcnow, index=True)
    time_spent_seconds = Column(Integer)  # 复习花费时间（秒）
    notes = Column(Text)  # 复习笔记
    
    # 关系
    knowledge_point = relationship("KnowledgePoint", back_populates="review_records")


class KnowledgeRelation(Base):
    """知识点关系模型 - 构建知识体系"""
    __tablename__ = "knowledge_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    child_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    
    # 关系类型：prerequisite(前置), related(相关), extends(扩展), applies_to(应用于)
    relation_type = Column(String(50), default="related")
    strength = Column(Float, default=1.0)  # 关系强度（0-1）
    description = Column(Text)  # 关系描述
    
    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_ai = Column(Boolean, default=False)  # 是否由AI生成
    
    # 关系
    parent = relationship(
        "KnowledgePoint",
        foreign_keys=[parent_id],
        back_populates="child_relations"
    )
    child = relationship(
        "KnowledgePoint",
        foreign_keys=[child_id],
        back_populates="parent_relations"
    )

