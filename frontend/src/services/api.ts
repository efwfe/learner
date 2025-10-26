import axios from 'axios';
import type {
  KnowledgePoint,
  LearningContent,
  ReviewRecord,
  ReviewPlan,
  KnowledgeGraph,
  KnowledgePointForm,
  LearningContentForm,
  ReviewForm,
} from '@/types';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 知识点 API
export const knowledgeApi = {
  list: async (params?: {
    category?: string;
    tag?: string;
    is_mastered?: boolean;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get<KnowledgePoint[]>('/knowledge/', { params });
    return response.data;
  },

  get: async (id: number) => {
    const response = await api.get<KnowledgePoint>(`/knowledge/${id}`);
    return response.data;
  },

  create: async (data: KnowledgePointForm, generateSummary: boolean = true) => {
    const response = await api.post<KnowledgePoint>('/knowledge/', data, {
      params: { generate_summary: generateSummary },
    });
    return response.data;
  },

  update: async (id: number, data: Partial<KnowledgePointForm>) => {
    const response = await api.put<KnowledgePoint>(`/knowledge/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/knowledge/${id}`);
  },

  getStats: async () => {
    const response = await api.get('/knowledge/stats/summary');
    return response.data;
  },
};

// 学习内容 API
export const learningApi = {
  list: async (params?: {
    knowledge_point_id?: number;
    days?: number;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get<LearningContent[]>('/learning/', { params });
    return response.data;
  },

  create: async (data: LearningContentForm, autoExtract: boolean = true) => {
    const response = await api.post<LearningContent>('/learning/', data, {
      params: { auto_extract: autoExtract },
    });
    return response.data;
  },

  getDailyStats: async (days: number = 30) => {
    const response = await api.get('/learning/stats/daily', {
      params: { days },
    });
    return response.data;
  },
};

// 复习 API
export const reviewApi = {
  create: async (data: ReviewForm) => {
    const response = await api.post<ReviewRecord>('/review/', data);
    return response.data;
  },

  getPlan: async (date?: string) => {
    const response = await api.get<ReviewPlan>('/review/plan', {
      params: { date },
    });
    return response.data;
  },

  getDueReviews: async (limit: number = 10) => {
    const response = await api.get<KnowledgePoint[]>('/review/due', {
      params: { limit },
    });
    return response.data;
  },

  generateQuestion: async (kpId: number) => {
    const response = await api.get(`/review/question/${kpId}`);
    return response.data;
  },

  getHistory: async (kpId: number, limit: number = 50) => {
    const response = await api.get<ReviewRecord[]>(`/review/history/${kpId}`, {
      params: { limit },
    });
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/review/stats/overall');
    return response.data;
  },
};

// 知识图谱 API
export const graphApi = {
  get: async (centerId?: number, depth: number = 2) => {
    const response = await api.get<KnowledgeGraph>('/graph/', {
      params: { center_id: centerId, depth },
    });
    return response.data;
  },

  suggestRelations: async (kpId: number, maxSuggestions: number = 5) => {
    const response = await api.get(`/graph/suggest/${kpId}`, {
      params: { max_suggestions: maxSuggestions },
    });
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/graph/categories');
    return response.data;
  },
};

// 健康检查
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

