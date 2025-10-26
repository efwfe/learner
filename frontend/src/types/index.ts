// API 类型定义

export interface KnowledgePoint {
  id: number;
  title: string;
  content: string;
  summary?: string;
  category?: string;
  tags?: string;
  ease_factor: number;
  interval: number;
  repetitions: number;
  next_review_date: string;
  created_at: string;
  updated_at: string;
  is_mastered: boolean;
}

export interface LearningContent {
  id: number;
  knowledge_point_id: number;
  content: string;
  source?: string;
  notes?: string;
  learning_date: string;
  created_at: string;
}

export interface ReviewRecord {
  id: number;
  knowledge_point_id: number;
  quality: number;
  ease_factor_before?: number;
  interval_before?: number;
  ease_factor_after?: number;
  interval_after?: number;
  reviewed_at: string;
  time_spent_seconds?: number;
  notes?: string;
}

export interface KnowledgeRelation {
  id: number;
  parent_id: number;
  child_id: number;
  relation_type: string;
  strength: number;
  description?: string;
  created_at: string;
  created_by_ai: boolean;
}

export interface ReviewPlan {
  date: string;
  total_reviews: number;
  estimated_time_minutes: number;
  reviews_by_priority: {
    high: KnowledgePoint[];
    medium: KnowledgePoint[];
    low: KnowledgePoint[];
  };
}

export interface KnowledgeGraphNode {
  id: number;
  title: string;
  category?: string;
  is_mastered: boolean;
  ease_factor: number;
  repetitions: number;
}

export interface KnowledgeGraphEdge {
  source: number;
  target: number;
  relation_type: string;
  strength: number;
}

export interface KnowledgeGraph {
  nodes: KnowledgeGraphNode[];
  edges: KnowledgeGraphEdge[];
}

// 表单类型
export interface KnowledgePointForm {
  title: string;
  content: string;
  category?: string;
  tags?: string;
}

export interface LearningContentForm {
  content: string;
  source?: string;
  notes?: string;
  knowledge_point_id?: number;
}

export interface ReviewForm {
  knowledge_point_id: number;
  quality: number;
  time_spent_seconds?: number;
  notes?: string;
}

