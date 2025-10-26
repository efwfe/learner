import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, BookOpen, Calendar, Network, Menu } from 'lucide-react';
import { useStore } from '@/hooks/useStore';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const { sidebarOpen, setSidebarOpen } = useStore();
  const { t } = useTranslation();

  const navItems = [
    { path: '/', icon: Home, label: t('nav.home') },
    { path: '/knowledge', icon: BookOpen, label: t('nav.knowledge') },
    { path: '/review', icon: Calendar, label: t('nav.review') },
    { path: '/graph', icon: Network, label: t('nav.graph') },
  ];

  return (
    <div className="layout">
      {/* 顶部导航栏 */}
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <button
              className="menu-btn"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              <Menu size={20} />
            </button>
            <h1 className="logo">Learner</h1>
          </div>
          <LanguageSwitcher />
        </div>
      </header>

      <div className="main-container">
        {/* 侧边栏 */}
        <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <nav className="nav">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-item ${isActive ? 'active' : ''}`}
                >
                  <Icon size={20} />
                  {sidebarOpen && <span>{item.label}</span>}
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* 主内容区域 */}
        <main className="content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;

