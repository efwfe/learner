"""
知识服务 - 处理知识点的CRUD和业务逻辑
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from ..models.knowledge import (
    KnowledgePoint, 
    LearningContent, 
    ReviewRecord,
    KnowledgeRelation
)
from ..schemas.knowledge import (
    KnowledgePointCreate,
    KnowledgePointUpdate,
    LearningContentCreate,
    ReviewRecordCreate,
    KnowledgeRelationCreate
)
from .spaced_repetition import SpacedRepetitionAlgorithm
from .openai_service import openai_service


class KnowledgeService:
    """知识点服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.sr_algorithm = SpacedRepetitionAlgorithm()
    
    # ========== 知识点 CRUD ==========
    
    def create_knowledge_point(
        self, 
        data: KnowledgePointCreate,
        generate_summary: bool = True
    ) -> KnowledgePoint:
        """创建知识点"""
        kp = KnowledgePoint(
            title=data.title,
            content=data.content,
            category=data.category,
            tags=data.tags
        )
        
        self.db.add(kp)
        self.db.commit()
        self.db.refresh(kp)
        
        # 异步生成摘要（如果启用）
        if generate_summary and openai_service.is_available():
            import asyncio
            summary = asyncio.run(
                openai_service.generate_knowledge_summary(kp.title, kp.content)
            )
            kp.summary = summary
            self.db.commit()
            self.db.refresh(kp)
        
        return kp
    
    def get_knowledge_point(self, kp_id: int) -> Optional[KnowledgePoint]:
        """获取知识点"""
        return self.db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_id).first()
    
    def list_knowledge_points(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        is_mastered: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[KnowledgePoint]:
        """列出知识点"""
        query = self.db.query(KnowledgePoint)
        
        if category:
            query = query.filter(KnowledgePoint.category == category)
        if tag:
            query = query.filter(KnowledgePoint.tags.contains(tag))
        if is_mastered is not None:
            query = query.filter(KnowledgePoint.is_mastered == is_mastered)
        
        return query.order_by(KnowledgePoint.created_at.desc()).offset(skip).limit(limit).all()
    
    def update_knowledge_point(
        self, 
        kp_id: int, 
        data: KnowledgePointUpdate
    ) -> Optional[KnowledgePoint]:
        """更新知识点"""
        kp = self.get_knowledge_point(kp_id)
        if not kp:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(kp, field, value)
        
        kp.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(kp)
        
        return kp
    
    def delete_knowledge_point(self, kp_id: int) -> bool:
        """删除知识点"""
        kp = self.get_knowledge_point(kp_id)
        if not kp:
            return False
        
        self.db.delete(kp)
        self.db.commit()
        return True
    
    # ========== 学习内容 ==========
    
    def create_learning_content(
        self,
        data: LearningContentCreate,
        auto_extract_knowledge: bool = True
    ) -> LearningContent:
        """创建学习内容"""
        # 如果没有指定知识点，尝试自动提取
        if not data.knowledge_point_id and auto_extract_knowledge:
            # 使用GPT提取知识点
            import asyncio
            extracted_points = asyncio.run(
                openai_service.extract_knowledge_points(data.content)
            )
            
            # 创建第一个提取的知识点
            if extracted_points:
                first_point = extracted_points[0]
                kp = self.create_knowledge_point(
                    KnowledgePointCreate(
                        title=first_point.get("title", "未命名知识点"),
                        content=first_point.get("content", data.content),
                        category=first_point.get("category")
                    )
                )
                data.knowledge_point_id = kp.id
        
        # 如果还是没有知识点ID，创建一个默认的
        if not data.knowledge_point_id:
            kp = self.create_knowledge_point(
                KnowledgePointCreate(
                    title=f"学习内容 {datetime.utcnow().strftime('%Y-%m-%d')}",
                    content=data.content
                )
            )
            data.knowledge_point_id = kp.id
        
        lc = LearningContent(
            knowledge_point_id=data.knowledge_point_id,
            content=data.content,
            source=data.source,
            notes=data.notes
        )
        
        self.db.add(lc)
        self.db.commit()
        self.db.refresh(lc)
        
        return lc
    
    # ========== 复习记录 ==========
    
    def create_review_record(self, data: ReviewRecordCreate) -> ReviewRecord:
        """创建复习记录并更新知识点的复习参数"""
        kp = self.get_knowledge_point(data.knowledge_point_id)
        if not kp:
            raise ValueError(f"知识点 {data.knowledge_point_id} 不存在")
        
        # 保存更新前的参数
        ease_factor_before = kp.ease_factor
        interval_before = kp.interval
        
        # 计算新的复习参数
        new_ease_factor, new_interval, new_repetitions, next_review_date = \
            self.sr_algorithm.calculate_next_review(
                quality=data.quality,
                ease_factor=kp.ease_factor,
                interval=kp.interval,
                repetitions=kp.repetitions
            )
        
        # 更新知识点
        kp.ease_factor = new_ease_factor
        kp.interval = new_interval
        kp.repetitions = new_repetitions
        kp.next_review_date = next_review_date
        kp.updated_at = datetime.utcnow()
        
        # 如果质量很高且重复次数多，标记为已掌握
        if data.quality >= 4 and new_repetitions >= 5:
            kp.is_mastered = True
        
        # 创建复习记录
        record = ReviewRecord(
            knowledge_point_id=data.knowledge_point_id,
            quality=data.quality,
            ease_factor_before=ease_factor_before,
            interval_before=interval_before,
            ease_factor_after=new_ease_factor,
            interval_after=new_interval,
            time_spent_seconds=data.time_spent_seconds,
            notes=data.notes
        )
        
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
        return record
    
    def get_daily_review_plan(self, date: datetime = None) -> Dict:
        """获取每日复习计划"""
        if date is None:
            date = datetime.utcnow()
        
        # 查询需要复习的知识点（未掌握的且复习日期已到）
        knowledge_points = self.db.query(KnowledgePoint).filter(
            and_(
                KnowledgePoint.is_mastered == False,
                KnowledgePoint.next_review_date <= date
            )
        ).all()
        
        # 按优先级分类
        reviews_by_priority = {
            "high": [],
            "medium": [],
            "low": []
        }
        
        total_time = 0
        for kp in knowledge_points:
            priority = self.sr_algorithm.get_priority_level(
                kp.next_review_date,
                kp.ease_factor
            )
            reviews_by_priority[priority].append(kp)
            
            # 累计预估时间
            time = self.sr_algorithm.estimate_review_time(
                kp.repetitions,
                kp.ease_factor
            )
            total_time += time
        
        return {
            "date": date,
            "total_reviews": len(knowledge_points),
            "reviews_by_priority": reviews_by_priority,
            "estimated_time_minutes": total_time
        }
    
    # ========== 知识关系 ==========
    
    def create_knowledge_relation(
        self,
        data: KnowledgeRelationCreate,
        created_by_ai: bool = False
    ) -> KnowledgeRelation:
        """创建知识关系"""
        relation = KnowledgeRelation(
            parent_id=data.parent_id,
            child_id=data.child_id,
            relation_type=data.relation_type,
            strength=data.strength,
            description=data.description,
            created_by_ai=created_by_ai
        )
        
        self.db.add(relation)
        self.db.commit()
        self.db.refresh(relation)
        
        return relation
    
    def get_knowledge_graph(self, center_id: Optional[int] = None, depth: int = 2) -> Dict:
        """获取知识图谱"""
        if center_id:
            # 获取以某个知识点为中心的子图
            center_kp = self.get_knowledge_point(center_id)
            if not center_kp:
                return {"nodes": [], "edges": []}
            
            # TODO: 实现基于深度的图遍历
            # 这里简化实现，返回直接相关的节点
            related_relations = self.db.query(KnowledgeRelation).filter(
                or_(
                    KnowledgeRelation.parent_id == center_id,
                    KnowledgeRelation.child_id == center_id
                )
            ).all()
            
            node_ids = {center_id}
            for rel in related_relations:
                node_ids.add(rel.parent_id)
                node_ids.add(rel.child_id)
            
            nodes = self.db.query(KnowledgePoint).filter(
                KnowledgePoint.id.in_(node_ids)
            ).all()
            
        else:
            # 获取全局图谱
            nodes = self.db.query(KnowledgePoint).all()
            related_relations = self.db.query(KnowledgeRelation).all()
        
        # 构建图数据
        graph_nodes = [
            {
                "id": kp.id,
                "title": kp.title,
                "category": kp.category,
                "is_mastered": kp.is_mastered,
                "ease_factor": kp.ease_factor,
                "repetitions": kp.repetitions
            }
            for kp in nodes
        ]
        
        graph_edges = [
            {
                "source": rel.parent_id,
                "target": rel.child_id,
                "relation_type": rel.relation_type,
                "strength": rel.strength
            }
            for rel in related_relations
        ]
        
        return {
            "nodes": graph_nodes,
            "edges": graph_edges
        }
    
    def auto_suggest_relations(self, kp_id: int, max_suggestions: int = 5) -> List[Dict]:
        """自动建议知识关系"""
        kp = self.get_knowledge_point(kp_id)
        if not kp:
            return []
        
        # 获取其他知识点
        other_kps = self.db.query(KnowledgePoint).filter(
            KnowledgePoint.id != kp_id
        ).limit(50).all()
        
        if not other_kps:
            return []
        
        # 使用GPT建议关系
        import asyncio
        suggestions = asyncio.run(
            openai_service.suggest_knowledge_relations(
                {
                    "id": kp.id,
                    "title": kp.title,
                    "content": kp.content,
                    "summary": kp.summary
                },
                [
                    {
                        "id": other_kp.id,
                        "title": other_kp.title,
                        "content": other_kp.content,
                        "summary": other_kp.summary
                    }
                    for other_kp in other_kps
                ]
            )
        )
        
        return suggestions[:max_suggestions]

