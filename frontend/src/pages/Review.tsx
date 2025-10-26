import React, { useEffect, useState } from 'react';
import { Calendar, Clock, CheckCircle } from 'lucide-react';
import { reviewApi } from '@/services/api';
import type { ReviewPlan, KnowledgePoint } from '@/types';
import { formatDate } from '@/utils/date';
import './Review.css';

const Review: React.FC = () => {
  const [plan, setPlan] = useState<ReviewPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentReview, setCurrentReview] = useState<KnowledgePoint | null>(null);
  const [quality, setQuality] = useState<number>(3);
  const [reviewing, setReviewing] = useState(false);

  useEffect(() => {
    loadReviewPlan();
  }, []);

  const loadReviewPlan = async () => {
    try {
      setLoading(true);
      const data = await reviewApi.getPlan();
      setPlan(data);
    } catch (error) {
      console.error('Failed to load review plan:', error);
    } finally {
      setLoading(false);
    }
  };

  const startReview = (kp: KnowledgePoint) => {
    setCurrentReview(kp);
    setQuality(3);
    setReviewing(true);
  };

  const submitReview = async () => {
    if (!currentReview) return;

    try {
      await reviewApi.create({
        knowledge_point_id: currentReview.id,
        quality,
      });
      setReviewing(false);
      setCurrentReview(null);
      // 重新加载复习计划
      await loadReviewPlan();
    } catch (error) {
      console.error('Failed to submit review:', error);
    }
  };

  const qualityLevels = [
    { value: 0, label: '完全不记得', color: 'var(--color-danger)' },
    { value: 1, label: '错误答案', color: '#ff6b6b' },
    { value: 2, label: '错误但想起来了', color: 'var(--color-warning)' },
    { value: 3, label: '困难但正确', color: '#ffd93d' },
    { value: 4, label: '犹豫后正确', color: '#6bcf7f' },
    { value: 5, label: '完美记忆', color: 'var(--color-success)' },
  ];

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  if (reviewing && currentReview) {
    return (
      <div className="review-session">
        <div className="review-card">
          <h2>复习：{currentReview.title}</h2>
          
          <div className="review-content">
            <p>{currentReview.content}</p>
            {currentReview.summary && (
              <div className="review-summary">
                <strong>摘要：</strong>
                <p>{currentReview.summary}</p>
              </div>
            )}
          </div>

          <div className="quality-selector">
            <h3>回忆质量评分</h3>
            <div className="quality-options">
              {qualityLevels.map((level) => (
                <button
                  key={level.value}
                  className={`quality-btn ${quality === level.value ? 'active' : ''}`}
                  style={{
                    '--quality-color': level.color,
                  } as React.CSSProperties}
                  onClick={() => setQuality(level.value)}
                >
                  <span className="quality-value">{level.value}</span>
                  <span className="quality-label">{level.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="review-actions">
            <button
              className="btn btn-secondary"
              onClick={() => setReviewing(false)}
            >
              取消
            </button>
            <button
              className="btn btn-primary"
              onClick={submitReview}
            >
              提交复习
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="review-page">
      <div className="page-header">
        <h1>今日复习计划</h1>
        <div className="plan-meta">
          <span className="meta-item">
            <Calendar size={16} />
            {plan && formatDate(plan.date)}
          </span>
          <span className="meta-item">
            <Clock size={16} />
            预计 {plan?.estimated_time_minutes || 0} 分钟
          </span>
        </div>
      </div>

      {plan && plan.total_reviews > 0 ? (
        <>
          <div className="priority-section">
            <h2 className="priority-title high">
              高优先级 ({plan.reviews_by_priority.high.length})
            </h2>
            <div className="review-list">
              {plan.reviews_by_priority.high.map((kp) => (
                <div key={kp.id} className="review-item card">
                  <div className="review-item-content">
                    <h3>{kp.title}</h3>
                    <p>{kp.summary || kp.content.substring(0, 100)}</p>
                    <div className="review-item-meta">
                      <span>复习 {kp.repetitions} 次</span>
                      <span>难度 {kp.ease_factor.toFixed(1)}</span>
                    </div>
                  </div>
                  <button
                    className="btn btn-primary"
                    onClick={() => startReview(kp)}
                  >
                    开始复习
                  </button>
                </div>
              ))}
            </div>
          </div>

          {plan.reviews_by_priority.medium.length > 0 && (
            <div className="priority-section">
              <h2 className="priority-title medium">
                中优先级 ({plan.reviews_by_priority.medium.length})
              </h2>
              <div className="review-list">
                {plan.reviews_by_priority.medium.map((kp) => (
                  <div key={kp.id} className="review-item card">
                    <div className="review-item-content">
                      <h3>{kp.title}</h3>
                      <p>{kp.summary || kp.content.substring(0, 100)}</p>
                    </div>
                    <button
                      className="btn btn-secondary"
                      onClick={() => startReview(kp)}
                    >
                      开始复习
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="empty-state">
          <CheckCircle size={64} color="var(--color-success)" />
          <h2>今天没有复习任务</h2>
          <p>太棒了！所有知识点都在掌握中</p>
        </div>
      )}
    </div>
  );
};

export default Review;

