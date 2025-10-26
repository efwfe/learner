import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Calendar, TrendingUp, CheckCircle } from 'lucide-react';
import { knowledgeApi, reviewApi } from '@/services/api';
import { useTranslation } from 'react-i18next';
import './Home.css';

interface Stats {
  total: number;
  mastered: number;
  in_progress: number;
  mastery_rate: number;
}

interface ReviewStats {
  due_reviews: number;
  reviewed_today: number;
  average_quality: number;
}

const Home: React.FC = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState<Stats | null>(null);
  const [reviewStats, setReviewStats] = useState<ReviewStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [knowledgeStats, reviewStatsData] = await Promise.all([
        knowledgeApi.getStats(),
        reviewApi.getStats(),
      ]);
      setStats(knowledgeStats);
      setReviewStats(reviewStatsData);
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">{t('common.loading')}</div>;
  }

  return (
    <div className="home">
      <div className="hero">
        <h1 className="hero-title fade-in">{t('home.title')}</h1>
        <p className="hero-subtitle fade-in">
          {t('home.subtitle')}
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-primary)' }}>
            <BookOpen size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total || 0}</div>
            <div className="stat-label">{t('home.stats.total')}</div>
          </div>
        </div>

        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-success)' }}>
            <CheckCircle size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.mastered || 0}</div>
            <div className="stat-label">{t('home.stats.mastered')}</div>
          </div>
        </div>

        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-warning)' }}>
            <Calendar size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">{reviewStats?.due_reviews || 0}</div>
            <div className="stat-label">{t('home.stats.dueReviews')}</div>
          </div>
        </div>

        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-danger)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">
              {stats?.mastery_rate?.toFixed(1) || 0}%
            </div>
            <div className="stat-label">{t('home.stats.masteryRate')}</div>
          </div>
        </div>
      </div>

      <div className="action-cards">
        <Link to="/knowledge" className="action-card card fade-in">
          <BookOpen size={32} />
          <h3>{t('home.actions.addLearning.title')}</h3>
          <p>{t('home.actions.addLearning.desc')}</p>
        </Link>

        <Link to="/review" className="action-card card fade-in">
          <Calendar size={32} />
          <h3>{t('home.actions.startReview.title')}</h3>
          <p>{t('home.actions.startReview.desc')}</p>
        </Link>

        <Link to="/graph" className="action-card card fade-in">
          <TrendingUp size={32} />
          <h3>{t('home.actions.viewGraph.title')}</h3>
          <p>{t('home.actions.viewGraph.desc')}</p>
        </Link>
      </div>

      <div className="quick-stats">
        <div className="quick-stat-item">
          <span className="quick-stat-label">{t('home.quickStats.reviewedToday')}</span>
          <span className="quick-stat-value">
            {reviewStats?.reviewed_today || 0} {t('home.quickStats.items')}
          </span>
        </div>
        <div className="quick-stat-item">
          <span className="quick-stat-label">{t('home.quickStats.avgQuality')}</span>
          <span className="quick-stat-value">
            {reviewStats?.average_quality?.toFixed(1) || 0} / 5
          </span>
        </div>
        <div className="quick-stat-item">
          <span className="quick-stat-label">{t('home.quickStats.inProgress')}</span>
          <span className="quick-stat-value">
            {stats?.in_progress || 0} {t('home.quickStats.items')}
          </span>
        </div>
      </div>
    </div>
  );
};

export default Home;

