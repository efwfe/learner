import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Calendar, TrendingUp, CheckCircle } from 'lucide-react';
import { knowledgeApi, reviewApi } from '@/services/api';
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
    return <div className="loading">加载中...</div>;
  }

  return (
    <div className="home">
      <div className="hero">
        <h1 className="hero-title fade-in">智能学习管理系统</h1>
        <p className="hero-subtitle fade-in">
          基于遗忘曲线的个人知识管理平台，帮助你构建系统化的知识体系
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-primary)' }}>
            <BookOpen size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total || 0}</div>
            <div className="stat-label">知识点总数</div>
          </div>
        </div>

        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-success)' }}>
            <CheckCircle size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.mastered || 0}</div>
            <div className="stat-label">已掌握</div>
          </div>
        </div>

        <div className="stat-card fade-in">
          <div className="stat-icon" style={{ background: 'var(--color-warning)' }}>
            <Calendar size={24} color="white" />
          </div>
          <div className="stat-content">
            <div className="stat-value">{reviewStats?.due_reviews || 0}</div>
            <div className="stat-label">待复习</div>
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
            <div className="stat-label">掌握率</div>
          </div>
        </div>
      </div>

      <div className="action-cards">
        <Link to="/knowledge" className="action-card card fade-in">
          <BookOpen size={32} />
          <h3>记录学习</h3>
          <p>添加今天的学习内容，系统会自动提取知识点</p>
        </Link>

        <Link to="/review" className="action-card card fade-in">
          <Calendar size={32} />
          <h3>开始复习</h3>
          <p>根据遗忘曲线，智能安排今日的复习计划</p>
        </Link>

        <Link to="/graph" className="action-card card fade-in">
          <TrendingUp size={32} />
          <h3>知识图谱</h3>
          <p>可视化你的知识体系，发现知识点之间的关联</p>
        </Link>
      </div>

      <div className="quick-stats">
        <div className="quick-stat-item">
          <span className="quick-stat-label">今日已复习</span>
          <span className="quick-stat-value">
            {reviewStats?.reviewed_today || 0} 个
          </span>
        </div>
        <div className="quick-stat-item">
          <span className="quick-stat-label">平均复习质量</span>
          <span className="quick-stat-value">
            {reviewStats?.average_quality?.toFixed(1) || 0} / 5
          </span>
        </div>
        <div className="quick-stat-item">
          <span className="quick-stat-label">学习中</span>
          <span className="quick-stat-value">
            {stats?.in_progress || 0} 个
          </span>
        </div>
      </div>
    </div>
  );
};

export default Home;

