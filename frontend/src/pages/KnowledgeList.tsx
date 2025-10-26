import React, { useEffect, useState } from 'react';
import { Plus, Search, Filter } from 'lucide-react';
import { knowledgeApi } from '@/services/api';
import { useStore } from '@/hooks/useStore';
// import type { KnowledgePoint } from '@/types';
import { formatRelativeTime } from '@/utils/date';
import { useTranslation } from 'react-i18next';
import KnowledgeForm from '@/components/KnowledgeForm';
import './KnowledgeList.css';

const KnowledgeList: React.FC = () => {
  const { t } = useTranslation();
  const { knowledgePoints, setKnowledgePoints } = useStore();
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [showForm, setShowForm] = useState(false);

  const loadKnowledgePoints = async () => {
    try {
      setLoading(true);
      const data = await knowledgeApi.list({
        category: selectedCategory || undefined,
      });
      setKnowledgePoints(data);
    } catch (error) {
      console.error('Failed to load knowledge points:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadKnowledgePoints();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCategory]);

  const filteredPoints = knowledgePoints.filter((kp) =>
    kp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    kp.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getProgressColor = (repetitions: number, is_mastered: boolean) => {
    if (is_mastered) return 'var(--color-success)';
    if (repetitions >= 3) return 'var(--color-primary)';
    if (repetitions >= 1) return 'var(--color-warning)';
    return 'var(--color-text-tertiary)';
  };

  return (
    <div className="knowledge-list-page">
      <div className="page-header">
        <h1>{t('knowledge.title')}</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>
          <Plus size={20} />
          {t('knowledge.addNew')}
        </button>
      </div>

      <div className="filters">
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder={t('knowledge.searchPlaceholder')}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input"
          />
        </div>

        <div className="filter-group">
          <Filter size={20} />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="input"
          >
            <option value="">{t('common.allCategories')}</option>
            <option value="编程">{t('knowledge.categories.programming')}</option>
            <option value="数学">{t('knowledge.categories.math')}</option>
            <option value="语言">{t('knowledge.categories.language')}</option>
            <option value="其他">{t('knowledge.categories.other')}</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading">{t('common.loading')}</div>
      ) : (
        <div className="knowledge-grid">
          {filteredPoints.map((kp) => (
            <div key={kp.id} className="knowledge-card card">
              <div className="knowledge-card-header">
                <h3>{kp.title}</h3>
                {kp.is_mastered && (
                  <span className="badge badge-success">{t('knowledge.mastered')}</span>
                )}
              </div>

              <p className="knowledge-summary">
                {kp.summary || kp.content.substring(0, 100) + '...'}
              </p>

              <div className="knowledge-meta">
                <span className="meta-item">
                  {t('knowledge.reviews')} {kp.repetitions} {t('knowledge.times')}
                </span>
                <span
                  className="meta-item"
                  style={{ color: getProgressColor(kp.repetitions, kp.is_mastered) }}
                >
                  {t('knowledge.difficulty')} {kp.ease_factor.toFixed(1)}
                </span>
              </div>

              <div className="knowledge-footer">
                <span className="timestamp">
                  {formatRelativeTime(kp.updated_at)}
                </span>
                {kp.category && (
                  <span className="category-tag">{kp.category}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && filteredPoints.length === 0 && (
        <div className="empty-state">
          <p>{t('knowledge.empty')}</p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>
            <Plus size={20} />
            {t('knowledge.createFirst')}
          </button>
        </div>
      )}

      <KnowledgeForm
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        onSuccess={loadKnowledgePoints}
      />
    </div>
  );
};

export default KnowledgeList;

