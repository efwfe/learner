import React, { useEffect, useState } from 'react';
import { Network, Filter } from 'lucide-react';
import { graphApi } from '@/services/api';
import type { KnowledgeGraph } from '@/types';
import { useTranslation } from 'react-i18next';
import './Graph.css';

const Graph: React.FC = () => {
  const { t } = useTranslation();
  const [graph, setGraph] = useState<KnowledgeGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  useEffect(() => {
    loadGraph();
  }, []);

  const loadGraph = async () => {
    try {
      setLoading(true);
      const data = await graphApi.get();
      setGraph(data);
    } catch (error) {
      console.error('Failed to load knowledge graph:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredNodes = graph?.nodes.filter(
    (node) => !selectedCategory || node.category === selectedCategory
  ) || [];

  const categories = Array.from(
    new Set(graph?.nodes.map((n) => n.category).filter(Boolean))
  );

  if (loading) {
    return <div className="loading">{t('common.loading')}</div>;
  }

  return (
    <div className="graph-page">
      <div className="page-header">
        <h1>{t('graph.title')}</h1>
        <div className="graph-controls">
          <div className="filter-group">
            <Filter size={20} />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input"
            >
              <option value="">{t('common.allCategories')}</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="graph-stats">
        <div className="stat-item">
          <span className="stat-label">知识点</span>
          <span className="stat-value">{filteredNodes.length}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">关系</span>
          <span className="stat-value">{graph?.edges.length || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">已掌握</span>
          <span className="stat-value">
            {filteredNodes.filter((n) => n.is_mastered).length}
          </span>
        </div>
      </div>

      <div className="graph-container card">
        <div className="graph-placeholder">
          <Network size={64} color="var(--color-text-tertiary)" />
          <p>知识图谱可视化</p>
          <p className="graph-note">
            此处将显示知识点之间的关系网络
            <br />
            需要集成 react-force-graph-2d 或类似库来实现
          </p>
        </div>
      </div>

      <div className="graph-legend">
        <h3>图例</h3>
        <div className="legend-items">
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ background: 'var(--color-success)' }}
            />
            <span>已掌握</span>
          </div>
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ background: 'var(--color-primary)' }}
            />
            <span>学习中</span>
          </div>
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ background: 'var(--color-warning)' }}
            />
            <span>需复习</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Graph;

