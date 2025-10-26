import React, { useState } from 'react';
import { X } from 'lucide-react';
import { knowledgeApi } from '@/services/api';
import type { KnowledgePointForm } from '@/types';
import './KnowledgeForm.css';

interface KnowledgeFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const KnowledgeForm: React.FC<KnowledgeFormProps> = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState<KnowledgePointForm>({
    title: '',
    content: '',
    category: '',
    tags: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.title.trim() || !formData.content.trim()) {
      setError('标题和内容不能为空');
      return;
    }

    try {
      setLoading(true);
      await knowledgeApi.create(formData, true);
      setFormData({ title: '', content: '', category: '', tags: '' });
      onSuccess();
      onClose();
    } catch (err) {
      setError('创建失败，请重试');
      console.error('Failed to create knowledge point:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      setFormData({ title: '', content: '', category: '', tags: '' });
      setError('');
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>新增知识点</h2>
          <button className="btn-icon" onClick={handleClose} disabled={loading}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="knowledge-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="title">标题 *</label>
            <input
              id="title"
              type="text"
              className="input"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="输入知识点标题"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="content">内容 *</label>
            <textarea
              id="content"
              className="input"
              rows={8}
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              placeholder="输入知识点详细内容"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">分类</label>
            <select
              id="category"
              className="input"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              disabled={loading}
            >
              <option value="">选择分类</option>
              <option value="编程">编程</option>
              <option value="数学">数学</option>
              <option value="语言">语言</option>
              <option value="其他">其他</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="tags">标签</label>
            <input
              id="tags"
              type="text"
              className="input"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              placeholder="用逗号分隔多个标签"
              disabled={loading}
            />
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={handleClose}
              disabled={loading}
            >
              取消
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? '创建中...' : '创建知识点'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default KnowledgeForm;

