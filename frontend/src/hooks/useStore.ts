import { create } from 'zustand';
import type { KnowledgePoint, ReviewPlan } from '@/types';

interface AppState {
  // 知识点列表
  knowledgePoints: KnowledgePoint[];
  setKnowledgePoints: (points: KnowledgePoint[]) => void;
  addKnowledgePoint: (point: KnowledgePoint) => void;
  updateKnowledgePoint: (id: number, point: Partial<KnowledgePoint>) => void;
  removeKnowledgePoint: (id: number) => void;

  // 当前选中的知识点
  selectedKnowledgePoint: KnowledgePoint | null;
  setSelectedKnowledgePoint: (point: KnowledgePoint | null) => void;

  // 复习计划
  reviewPlan: ReviewPlan | null;
  setReviewPlan: (plan: ReviewPlan | null) => void;

  // UI 状态
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

export const useStore = create<AppState>((set) => ({
  // 知识点列表
  knowledgePoints: [],
  setKnowledgePoints: (points) => set({ knowledgePoints: points }),
  addKnowledgePoint: (point) =>
    set((state) => ({
      knowledgePoints: [point, ...state.knowledgePoints],
    })),
  updateKnowledgePoint: (id, updates) =>
    set((state) => ({
      knowledgePoints: state.knowledgePoints.map((kp) =>
        kp.id === id ? { ...kp, ...updates } : kp
      ),
    })),
  removeKnowledgePoint: (id) =>
    set((state) => ({
      knowledgePoints: state.knowledgePoints.filter((kp) => kp.id !== id),
    })),

  // 当前选中的知识点
  selectedKnowledgePoint: null,
  setSelectedKnowledgePoint: (point) =>
    set({ selectedKnowledgePoint: point }),

  // 复习计划
  reviewPlan: null,
  setReviewPlan: (plan) => set({ reviewPlan: plan }),

  // UI 状态
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}));

