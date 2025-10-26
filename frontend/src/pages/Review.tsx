import React, { useEffect, useState } from 'react';
import { Calendar, Clock, CheckCircle } from 'lucide-react';
import { reviewApi } from '@/services/api';
import type { ReviewPlan, KnowledgePoint } from '@/types';
import { formatDate } from '@/utils/date';
import { useTranslation } from 'react-i18next';
import './Review.css';

const Review: React.FC = () => {
  const { t } = useTranslation();
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
    { value: 0, label: t('review.qualityLevels.0'), color: 'var(--color-danger)' },
    { value: 1, label: t('review.qualityLevels.1'), color: '#ff6b6b' },
    { value: 2, label: t('review.qualityLevels.2'), color: 'var(--color-warning)' },
    { value: 3, label: t('review.qualityLevels.3'), color: '#ffd93d' },
    { value: 4, label: t('review.qualityLevels.4'), color: '#6bcf7f' },
    { value: 5, label: t('review.qualityLevels.5'), color: 'var(--color-success)' },
  ];

  if (loading) {
    return <div className="loading">{t('common.loading')}</div>;
  }

  if (reviewing && currentReview) {
    return (
      <div className="review-session">
        <div className="review-card">
          <h2>{t('review.reviewing')}{currentReview.title}</h2>
          
          <div className="review-content">
            <p>{currentReview.content}</p>
            {currentReview.summary && (
              <div className="review-summary">
                <strong>{t('review.summary')}</strong>
                <p>{currentReview.summary}</p>
              </div>
            )}
          </div>

          <div className="quality-selector">
            <h3>{t('review.qualityRating')}</h3>
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
              {t('common.cancel')}
            </button>
            <button
              className="btn btn-primary"
              onClick={submitReview}
            >
              {t('review.submitReview')}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="review-page">
      <div className="page-header">
        <h1>{t('review.title')}</h1>
        <div className="plan-meta">
          <span className="meta-item">
            <Calendar size={16} />
            {plan && formatDate(plan.date)}
          </span>
          <span className="meta-item">
            <Clock size={16} />
            {t('review.estimatedTime')} {plan?.estimated_time_minutes || 0} {t('review.minutes')}
          </span>
        </div>
      </div>

      {plan && plan.total_reviews > 0 ? (
        <>
          <div className="priority-section">
            <h2 className="priority-title high">
              {t('review.highPriority')} ({plan.reviews_by_priority.high.length})
            </h2>
            <div className="review-list">
              {plan.reviews_by_priority.high.map((kp) => (
                <div key={kp.id} className="review-item card">
                  <div className="review-item-content">
                    <h3>{kp.title}</h3>
                    <p>{kp.summary || kp.content.substring(0, 100)}</p>
                    <div className="review-item-meta">
                      <span>{t('knowledge.reviews')} {kp.repetitions} {t('knowledge.times')}</span>
                      <span>{t('knowledge.difficulty')} {kp.ease_factor.toFixed(1)}</span>
                    </div>
                  </div>
                  <button
                    className="btn btn-primary"
                    onClick={() => startReview(kp)}
                  >
                    {t('review.startReview')}
                  </button>
                </div>
              ))}
            </div>
          </div>

          {plan.reviews_by_priority.medium.length > 0 && (
            <div className="priority-section">
              <h2 className="priority-title medium">
                {t('review.mediumPriority')} ({plan.reviews_by_priority.medium.length})
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
                      {t('review.startReview')}
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
          <h2>{t('review.noTasks.title')}</h2>
          <p>{t('review.noTasks.desc')}</p>
        </div>
      )}
    </div>
  );
};

export default Review;

