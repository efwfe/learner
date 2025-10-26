import React from 'react';
import { useTranslation } from 'react-i18next';
import { Languages } from 'lucide-react';
import './LanguageSwitcher.css';

const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'zh-CN' ? 'en-US' : 'zh-CN';
    i18n.changeLanguage(newLang);
  };

  return (
    <button className="language-switcher" onClick={toggleLanguage} title="Switch Language">
      <Languages size={20} />
      <span>{i18n.language === 'zh-CN' ? 'EN' : '中文'}</span>
    </button>
  );
};

export default LanguageSwitcher;

