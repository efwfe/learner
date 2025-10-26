# 系统架构文档

## 系统概览

Learner 是一个基于遗忘曲线的智能学习管理系统，采用前后端分离架构，使用 Docker 容器化部署。

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户界面层                          │
│                   React + TypeScript                    │
│           (Apple-style Minimalist Design)              │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                      API 网关层                          │
│                   FastAPI (Python)                      │
│               CORS + 认证 + 路由分发                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    业务逻辑层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 知识管理服务  │  │ 复习计划服务  │  │ 图谱服务      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │ 遗忘曲线算法  │  │ OpenAI 服务  │                    │
│  │   (SM-2)     │  │   (GPT-4)    │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    数据访问层                            │
│                   SQLAlchemy ORM                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    数据存储层                            │
│                   SQLite / PostgreSQL                   │
└─────────────────────────────────────────────────────────┘
```

## 核心模块

### 1. 遗忘曲线算法 (SuperMemo SM-2)

**文件**: `backend/app/services/spaced_repetition.py`

**核心参数**:
- `ease_factor`: 难易度因子 (初始值 2.5)
- `interval`: 复习间隔（天）
- `repetitions`: 重复次数
- `quality`: 复习质量评分 (0-5)

**算法流程**:
```python
if quality < 3:
    # 重置学习
    repetitions = 0
    interval = 1
else:
    repetitions += 1
    if repetitions == 1:
        interval = 1
    elif repetitions == 2:
        interval = 6
    else:
        interval = interval * ease_factor

# 调整难易度
ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
ease_factor = max(1.3, ease_factor)

next_review = today + interval days
```

### 2. AI 服务集成

**文件**: `backend/app/services/openai_service.py`

**功能**:
1. **知识点摘要生成**: 自动生成简洁的知识点摘要
2. **知识提取**: 从学习内容中提取关键知识点
3. **关系建议**: AI 分析并建议知识点之间的关系
4. **复习问题生成**: 根据知识点生成复习问题

**API 调用流程**:
```
用户输入 → OpenAI Service → Azure OpenAI API (GPT-4) → 解析响应 → 返回结果
```

### 3. 知识图谱

**数据结构**:
```typescript
interface KnowledgeGraph {
  nodes: KnowledgeGraphNode[];  // 知识点节点
  edges: KnowledgeGraphEdge[];  // 关系边
}
```

**关系类型**:
- `prerequisite`: 前置知识（A 是 B 的基础）
- `related`: 相关知识（A 和 B 主题相关）
- `extends`: 扩展知识（B 是 A 的深入）
- `applies_to`: 应用场景（A 可应用于 B）

## 数据模型

### 核心实体关系图

```
┌─────────────────┐
│ KnowledgePoint  │
│  - id           │
│  - title        │◄─────────┐
│  - content      │          │
│  - ease_factor  │          │
│  - interval     │          │
│  - repetitions  │          │
└─────────────────┘          │
        ▲                    │
        │                    │
        │ 1:N                │
        │                    │
┌─────────────────┐          │
│ LearningContent │          │
│  - id           │          │
│  - content      │          │
│  - notes        │          │
└─────────────────┘          │
                             │
        ▲                    │
        │                    │
        │ 1:N                │
        │                    │
┌─────────────────┐          │
│  ReviewRecord   │          │
│  - id           │          │
│  - quality      │          │
│  - reviewed_at  │          │
└─────────────────┘          │
                             │
                             │
┌─────────────────┐          │
│KnowledgeRelation│          │
│  - parent_id    ├──────────┘
│  - child_id     ├──────────┐
│  - type         │          │
│  - strength     │          │
└─────────────────┘          │
                             │
                             │
                             └────────┐
                                      ▼
                             ┌─────────────────┐
                             │ KnowledgePoint  │
                             └─────────────────┘
```

## API 设计

### RESTful API 结构

```
/api/v1/
├── knowledge/              # 知识点管理
│   ├── GET    /           # 列表
│   ├── POST   /           # 创建
│   ├── GET    /{id}       # 详情
│   ├── PUT    /{id}       # 更新
│   ├── DELETE /{id}       # 删除
│   └── GET    /stats/summary  # 统计
│
├── learning/              # 学习内容
│   ├── POST   /           # 创建
│   ├── GET    /           # 列表
│   └── GET    /stats/daily    # 统计
│
├── review/                # 复习管理
│   ├── POST   /           # 提交复习
│   ├── GET    /plan       # 复习计划
│   ├── GET    /due        # 待复习
│   ├── GET    /question/{id}  # 生成问题
│   ├── GET    /history/{id}   # 历史记录
│   └── GET    /stats/overall  # 统计
│
└── graph/                 # 知识图谱
    ├── GET    /           # 获取图谱
    ├── POST   /relations  # 创建关系
    ├── GET    /suggest/{id}    # AI 建议
    └── GET    /categories      # 分类统计
```

## 前端架构

### 组件层次结构

```
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   └── MenuButton
│   ├── Sidebar
│   │   └── Navigation
│   └── Content
│       └── [Page Components]
│
├── Pages
│   ├── Home
│   │   ├── HeroSection
│   │   ├── StatsCards
│   │   ├── ActionCards
│   │   └── QuickStats
│   │
│   ├── KnowledgeList
│   │   ├── SearchBar
│   │   ├── FilterBar
│   │   └── KnowledgeGrid
│   │       └── KnowledgeCard
│   │
│   ├── Review
│   │   ├── ReviewPlan
│   │   ├── ReviewList
│   │   │   └── ReviewItem
│   │   └── ReviewSession
│   │       └── QualitySelector
│   │
│   └── Graph
│       ├── GraphContainer
│       ├── GraphControls
│       └── GraphLegend
│
└── Services
    ├── api.ts          # API 调用
    ├── useStore.ts     # 状态管理
    └── date.ts         # 工具函数
```

### 状态管理 (Zustand)

```typescript
interface AppState {
  // 数据状态
  knowledgePoints: KnowledgePoint[];
  selectedKnowledgePoint: KnowledgePoint | null;
  reviewPlan: ReviewPlan | null;
  
  // UI 状态
  sidebarOpen: boolean;
  
  // 操作方法
  setKnowledgePoints: (points) => void;
  addKnowledgePoint: (point) => void;
  updateKnowledgePoint: (id, updates) => void;
  // ...
}
```

## 部署架构

### Docker 容器结构

```
Docker Host
├── learner-frontend (Container)
│   ├── Nginx (Port 80)
│   └── React Build
│
├── learner-backend (Container)
│   ├── Uvicorn (Port 8000)
│   └── FastAPI App
│
└── learner-network (Bridge Network)
```

### 网络通信

```
用户浏览器
    ↓ :3000
┌─────────────┐
│   Nginx     │
│  (Frontend) │
└─────────────┘
    ↓ /api → proxy to backend:8000
┌─────────────┐
│  Uvicorn    │
│  (Backend)  │
└─────────────┘
    ↓
┌─────────────┐
│   SQLite    │
└─────────────┘
```

## 安全考虑

1. **API 安全**
   - CORS 配置限制访问源
   - 可选的 JWT 认证
   - 输入验证和清理

2. **数据安全**
   - 环境变量存储敏感信息
   - .gitignore 防止泄露
   - Docker secrets 管理密钥

3. **前端安全**
   - XSS 防护
   - HTTPS 部署（生产环境）
   - CSP 策略

## 性能优化

1. **后端优化**
   - 数据库查询优化
   - 异步处理
   - 缓存策略

2. **前端优化**
   - 代码分割
   - 懒加载
   - 静态资源缓存
   - Gzip 压缩

3. **数据库优化**
   - 索引优化
   - 查询优化
   - 连接池管理

## 扩展性

### 水平扩展

```
Load Balancer
    ↓
┌───────┬───────┬───────┐
│ App 1 │ App 2 │ App 3 │
└───────┴───────┴───────┘
         ↓
   Shared Database
```

### 功能扩展点

1. **认证系统**: 添加用户注册/登录
2. **协作功能**: 知识点分享和协作
3. **数据分析**: 学习效果分析仪表板
4. **移动应用**: React Native 移动端
5. **插件系统**: 支持第三方扩展

## 监控和日志

1. **应用日志**: 结构化日志记录
2. **性能监控**: 响应时间追踪
3. **错误追踪**: 异常捕获和报告
4. **用户行为**: 学习数据分析

## 参考资源

- [SuperMemo Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

