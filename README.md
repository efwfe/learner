# Learner - Intelligent Learning Management System

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## 🌟 Overview

A personal knowledge management platform based on the forgetting curve, helping you build a systematic knowledge base with spaced repetition and AI-powered features.

## ✨ Core Features

### 1. Learning Content Management
- 📝 Record daily learning content
- 🤖 AI-powered knowledge point extraction
- 🏷️ Intelligent categorization and tag management

### 2. Intelligent Review System
- 📊 **SuperMemo SM-2** algorithm-based spaced repetition
- ⏰ Personalized review schedule
- 📈 Learning progress tracking

### 3. Knowledge Graph
- 🕸️ Visualize relationships between knowledge points
- 🔗 AI-powered intelligent association suggestions
- 🎯 Knowledge system construction

### 4. AI-Assisted Features
- 💡 Auto-generate knowledge summaries
- ❓ Intelligent review question generation
- 🤝 Knowledge relationship recommendations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM database management
- **Azure OpenAI** - GPT-4 AI integration
- **SQLite** - Lightweight database

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Zustand** - State management
- **Lucide Icons** - Icon library

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📦 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd learner
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your Azure OpenAI configuration
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env file

# Start service
python -m app.main
```

Backend service will start at http://localhost:8000

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend application will start at http://localhost:3000

## 📖 Usage Guide

### 1. Configure Azure OpenAI

Configure in the `.env` file:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 2. Add Learning Content

- Visit the "Knowledge Base" page
- Click "Add Knowledge Point"
- Enter learning content; the system will automatically extract key knowledge points using GPT

### 3. Start Reviewing

- Visit the "Review Plan" page
- View today's knowledge points to review
- Review by priority and rate (0-5 points)
- The system will automatically adjust the next review time based on your rating

### 4. Explore Knowledge Graph

- Visit the "Knowledge Graph" page
- View the network of relationships between knowledge points
- Use AI suggestion features to discover potential associations

## 🧠 Forgetting Curve Algorithm

This system uses the **SuperMemo SM-2** algorithm, a scientifically validated spaced repetition learning algorithm.

### Review Quality Rating

- **5** - Perfect recall: Effortless recall
- **4** - Correct after hesitation: Correct answer after thinking
- **3** - Difficult but correct: Recall with effort
- **2** - Wrong but remembered: Wrong answer but recalled with hints
- **1** - Wrong answer: Completely wrong
- **0** - Complete blackout: No memory at all

### Algorithm Features

- Dynamically adjusts review intervals based on review quality
- Higher quality = longer intervals
- Low quality (< 3) resets learning progress
- Personalized adaptation to each knowledge point's difficulty

## 📁 Project Structure

```
learner/
├── backend/                 # Backend code
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database configuration
│   │   ├── models/         # Data models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
│
├── frontend/               # Frontend code
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom hooks
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Utility functions
│   │   └── styles/        # Style files
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml      # Docker orchestration
└── README.md
```

## 🔧 API Documentation

After starting the backend service, visit the following addresses for complete API documentation:

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Main API Endpoints

#### Knowledge Management
- `GET /api/v1/knowledge/` - List knowledge points
- `POST /api/v1/knowledge/` - Create knowledge point
- `GET /api/v1/knowledge/{id}` - Get knowledge point details
- `PUT /api/v1/knowledge/{id}` - Update knowledge point
- `DELETE /api/v1/knowledge/{id}` - Delete knowledge point

#### Learning Content
- `POST /api/v1/learning/` - Add learning content
- `GET /api/v1/learning/` - View learning records
- `GET /api/v1/learning/stats/daily` - Learning statistics

#### Review Management
- `GET /api/v1/review/plan` - Get review plan
- `GET /api/v1/review/due` - Due reviews list
- `POST /api/v1/review/` - Submit review record
- `GET /api/v1/review/question/{id}` - Generate review question

#### Knowledge Graph
- `GET /api/v1/graph/` - Get knowledge graph
- `GET /api/v1/graph/suggest/{id}` - AI relationship suggestions
- `GET /api/v1/graph/categories` - Knowledge category statistics

## 🎨 UI Design

The interface adopts an **Apple-style minimalist design** with features including:

- 🎨 Clean and elegant visual style
- 🌓 Light/dark mode support
- 📱 Responsive design with mobile support
- ✨ Smooth animation transitions
- 🎯 User experience-focused interaction design

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 🙏 Acknowledgements

- [SuperMemo](https://www.supermemo.com/) - SM-2 algorithm
- [FastAPI](https://fastapi.tiangolo.com/) - Excellent web framework
- [React](https://react.dev/) - Powerful frontend framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - AI capabilities

---

💡 **Tip**: This is a personal knowledge management tool. It's recommended to use it daily to develop good learning and review habits!

---

<a name="chinese"></a>

# Learner - 智能学习管理系统

基于遗忘曲线的个人知识管理平台，帮助你构建系统化的知识体系。

## 🌟 核心功能

### 1. 学习内容管理
- 📝 记录每日学习内容
- 🤖 AI 自动提取知识点
- 🏷️ 智能分类和标签管理

### 2. 智能复习系统
- 📊 基于 **SuperMemo SM-2** 算法的间隔重复
- ⏰ 个性化复习计划
- 📈 学习进度追踪

### 3. 知识图谱
- 🕸️ 可视化知识点关系
- 🔗 AI 智能关联建议
- 🎯 知识体系构建

### 4. AI 辅助功能
- 💡 自动生成知识点摘要
- ❓ 智能复习问题生成
- 🤝 知识关系推荐

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **SQLAlchemy** - ORM 数据库管理
- **Azure OpenAI** - GPT-4 AI 能力集成
- **SQLite** - 轻量级数据库

### 前端
- **React 18** - 用户界面框架
- **TypeScript** - 类型安全
- **Vite** - 快速构建工具
- **Zustand** - 状态管理
- **Lucide Icons** - 图标库

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排

## 📦 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose（可选）

### 使用 Docker（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd learner
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 Azure OpenAI 配置
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问应用**
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/api/docs

### 本地开发

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
python -m app.main
```

后端服务将在 http://localhost:8000 启动

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:3000 启动

## 📖 使用指南

### 1. 配置 Azure OpenAI

在 `.env` 文件中配置：

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 2. 添加学习内容

- 访问"知识库"页面
- 点击"新增知识点"
- 输入学习内容，系统会自动使用 GPT 提取关键知识点

### 3. 开始复习

- 访问"复习计划"页面
- 查看今日待复习的知识点
- 按优先级进行复习，并评分（0-5分）
- 系统会根据评分自动调整下次复习时间

### 4. 探索知识图谱

- 访问"知识图谱"页面
- 查看知识点之间的关系网络
- 使用 AI 建议功能发现潜在关联

## 🧠 遗忘曲线算法

本系统采用 **SuperMemo SM-2** 算法，这是一个经过科学验证的间隔重复学习算法。

### 复习质量评分

- **5** - 完美记忆：毫不费力就能回忆起来
- **4** - 犹豫后正确：经过思考能正确回答
- **3** - 困难但正确：经过努力能想起来
- **2** - 错误但想起来了：答错但经提示能回忆
- **1** - 错误答案：完全答错
- **0** - 完全不记得：没有任何印象

### 算法特点

- 根据复习质量动态调整复习间隔
- 质量越高，间隔越长
- 质量低（< 3）会重置学习进度
- 个性化适应每个知识点的难度

## 📁 项目结构

```
learner/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模式
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 应用入口
│   ├── requirements.txt    # Python 依赖
│   └── Dockerfile
│
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/    # React 组件
│   │   ├── pages/         # 页面组件
│   │   ├── services/      # API 服务
│   │   ├── hooks/         # 自定义 Hooks
│   │   ├── types/         # TypeScript 类型
│   │   ├── utils/         # 工具函数
│   │   └── styles/        # 样式文件
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml      # Docker 编排
└── README.md
```

## 🔧 API 文档

启动后端服务后，访问以下地址查看完整 API 文档：

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 主要 API 端点

#### 知识点管理
- `GET /api/v1/knowledge/` - 列出知识点
- `POST /api/v1/knowledge/` - 创建知识点
- `GET /api/v1/knowledge/{id}` - 获取知识点详情
- `PUT /api/v1/knowledge/{id}` - 更新知识点
- `DELETE /api/v1/knowledge/{id}` - 删除知识点

#### 学习内容
- `POST /api/v1/learning/` - 添加学习内容
- `GET /api/v1/learning/` - 查看学习记录
- `GET /api/v1/learning/stats/daily` - 学习统计

#### 复习管理
- `GET /api/v1/review/plan` - 获取复习计划
- `GET /api/v1/review/due` - 待复习列表
- `POST /api/v1/review/` - 提交复习记录
- `GET /api/v1/review/question/{id}` - 生成复习问题

#### 知识图谱
- `GET /api/v1/graph/` - 获取知识图谱
- `GET /api/v1/graph/suggest/{id}` - AI 关系建议
- `GET /api/v1/graph/categories` - 知识分类统计

## 🎨 UI 设计

界面采用**苹果风格的极简设计**，特点包括：

- 🎨 简洁优雅的视觉风格
- 🌓 支持亮色/暗色模式
- 📱 响应式设计，支持移动端
- ✨ 流畅的动画过渡
- 🎯 注重用户体验的交互设计

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [SuperMemo](https://www.supermemo.com/) - SM-2 算法
- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的 Web 框架
- [React](https://react.dev/) - 强大的前端框架
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - AI 能力支持

---

💡 **提示**: 这是一个个人知识管理工具，建议坚持每日使用，养成良好的学习和复习习惯！
