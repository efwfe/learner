import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import KnowledgeList from './pages/KnowledgeList';
import Review from './pages/Review';
import Graph from './pages/Graph';
import './i18n';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/knowledge" element={<KnowledgeList />} />
          <Route path="/review" element={<Review />} />
          <Route path="/graph" element={<Graph />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;

