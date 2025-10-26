# 快速启动指南

## 5分钟快速开始

### 第一步：克隆或下载项目

```bash
git clone <repository-url>
cd learner
```

### 第二步：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入 Azure OpenAI 配置
nano .env
```

**最小配置示例：**
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

> 💡 **没有 Azure OpenAI？** 可以留空，基础功能仍可使用，只是无法使用 AI 辅助功能。

### 第三步：启动服务

**方式一：使用 Python 脚本（推荐）**
```bash
python main.py
```

**方式二：使用启动脚本**
```bash
./start-dev.sh
```

**方式三：手动启动 Docker**
```bash
docker-compose up -d
```

### 第四步：访问应用

打开浏览器访问：
- **应用界面**: http://localhost:3000
- **API 文档**: http://localhost:8000/api/docs

## 开始使用

### 1️⃣ 添加第一个知识点

1. 点击"知识库" → "新增知识点"
2. 输入标题和内容
3. 系统会自动生成摘要（需要配置 Azure OpenAI）

### 2️⃣ 开始复习

1. 点击"复习计划"
2. 查看今日待复习项目
3. 点击"开始复习"并评分（0-5分）
4. 系统会自动计算下次复习时间

### 3️⃣ 查看知识图谱

1. 点击"知识图谱"
2. 查看知识点之间的关系
3. 使用 AI 建议功能发现关联（需要 Azure OpenAI）

## 停止服务

```bash
# 使用 Docker Compose
docker-compose down

# 如果使用启动脚本，按 Ctrl+C
```

## 常见问题

### Q: 端口被占用？
**A:** 编辑 `docker-compose.yml` 修改端口映射：
```yaml
ports:
  - "3001:80"   # 前端改为 3001
  - "8001:8000" # 后端改为 8001
```

### Q: Docker 命令找不到？
**A:** 请先安装 Docker Desktop:
- macOS: https://docs.docker.com/desktop/install/mac-install/
- Windows: https://docs.docker.com/desktop/install/windows-install/
- Linux: https://docs.docker.com/engine/install/

### Q: 没有 Azure OpenAI 怎么办？
**A:** 不影响基础功能！你可以：
- ✅ 手动创建和管理知识点
- ✅ 使用遗忘曲线复习系统
- ✅ 查看和管理知识图谱
- ❌ 无法使用自动摘要生成
- ❌ 无法使用 AI 关系建议

### Q: 如何查看日志？
**A:** 
```bash
# 查看所有日志
docker-compose logs -f

# 只看后端
docker-compose logs -f backend

# 只看前端
docker-compose logs -f frontend
```

## 下一步

- 📖 阅读完整文档: [README.md](README.md)
- 🔧 详细设置指南: [SETUP.md](SETUP.md)
- 🐛 遇到问题？提交 Issue

---

💡 **小提示**: 建议每天花10-15分钟复习，系统会根据遗忘曲线自动优化你的学习效率！

