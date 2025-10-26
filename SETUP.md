# Learner 设置指南

## 快速开始

### 方式一：使用 Docker（推荐）

这是最简单的方式，只需要安装 Docker。

1. **配置环境变量**

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 Azure OpenAI 配置
nano .env  # 或使用其他编辑器
```

2. **启动服务**

```bash
# 使用启动脚本
./start-dev.sh

# 或手动启动
docker-compose up -d
```

3. **访问应用**

- 前端：http://localhost:3000
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/api/docs

### 方式二：本地开发

如果你想在本地开发环境运行，不使用 Docker：

1. **安装依赖**

确保已安装：
- Python 3.11+
- Node.js 18+

2. **后端设置**

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
python -m app.main
```

3. **前端设置**

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## Azure OpenAI 配置

### 获取 Azure OpenAI 访问权限

1. 访问 [Azure Portal](https://portal.azure.com)
2. 创建 Azure OpenAI 资源
3. 部署 GPT-4 模型
4. 获取以下信息：
   - Endpoint URL
   - API Key
   - Deployment Name

### 配置 .env 文件

```env
# Azure OpenAI 配置
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 没有 Azure OpenAI？

如果暂时没有 Azure OpenAI 访问权限，系统仍然可以正常运行，但以下功能将不可用：

- 自动生成知识点摘要
- 从学习内容自动提取知识点
- AI 智能关系建议
- 自动生成复习问题

你仍然可以：
- 手动创建和管理知识点
- 使用遗忘曲线复习系统
- 查看知识图谱
- 手动建立知识点关系

## 常见问题

### 1. 端口冲突

如果 3000 或 8000 端口已被占用，可以修改 `docker-compose.yml`：

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 改为 8001
  frontend:
    ports:
      - "3001:80"    # 改为 3001
```

### 2. 数据库初始化

首次运行时，数据库会自动创建。如果需要重置数据库：

```bash
# 删除数据库文件
rm backend/learner.db

# 重启服务
docker-compose restart backend
```

### 3. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 只查看后端日志
docker-compose logs -f backend

# 只查看前端日志
docker-compose logs -f frontend
```

### 4. 停止服务

```bash
# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

## 开发建议

### 后端开发

1. **安装开发工具**
```bash
pip install black flake8 pytest
```

2. **代码格式化**
```bash
black backend/app
```

3. **运行测试**
```bash
pytest backend/tests
```

### 前端开发

1. **安装开发工具**
```bash
npm install -g eslint prettier
```

2. **代码检查**
```bash
npm run lint
```

3. **构建生产版本**
```bash
npm run build
```

## 生产部署

### 使用 Docker Compose

1. 确保 `.env` 文件配置正确
2. 运行：
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 环境变量

生产环境需要设置：

```env
# 修改为生产数据库
DATABASE_URL=postgresql://user:password@localhost/learner

# 修改为强密码
SECRET_KEY=your-strong-secret-key-here

# 设置允许的源
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

## 更多帮助

- 📖 查看 [README.md](README.md) 了解功能详情
- 🐛 遇到问题？提交 [Issue](https://github.com/yourusername/learner/issues)
- 💬 需要帮助？查看 [Discussions](https://github.com/yourusername/learner/discussions)

