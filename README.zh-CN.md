# Learner - 智能学习管理系统

[English](README.md) | [中文](#chinese)

<a name="chinese"></a>

基于遗忘曲线的个人知识管理平台，帮助你构建系统化的知识体系。

## ✨ 核心功能

- 📝 **学习内容管理** - 记录每日学习内容，AI自动提取知识点
- 📊 **智能复习系统** - 基于 **SuperMemo SM-2** 算法的间隔重复
- 🕸️ **知识图谱** - 可视化知识点关系网络
- 🤖 **AI辅助** - 自动生成摘要和关系推荐

## 🚀 快速开始

### Docker部署（推荐）

```bash
# 克隆并配置
git clone <repository-url>
cd learner
cp .env.example .env
# 编辑 .env 填入 Azure OpenAI 配置

# 启动服务
docker-compose up -d
```

**访问地址：** http://localhost:3000

### 本地开发

**后端：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

## 🛠️ 技术栈

- **后端**：FastAPI、SQLAlchemy、Azure OpenAI、SQLite
- **前端**：React 18、TypeScript、Vite、Zustand、i18next
- **部署**：Docker、Docker Compose

## 📖 使用指南

1. **配置Azure OpenAI** - 在`.env`文件中配置
2. **添加知识点** - 访问知识库页面创建知识点
3. **开始复习** - 按照SM-2算法的复习计划进行
4. **探索图谱** - 可视化知识点关系网络

## 🌐 国际化支持

应用支持中英文双语。点击右上角的语言切换按钮即可切换语言。

## 📋 API文档

- Swagger UI：http://localhost:8000/api/docs
- ReDoc：http://localhost:8000/api/redoc

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

💡 **详细文档：**
- [快速开始指南](QUICKSTART.md)
- [架构概览](ARCHITECTURE.md)
- [项目摘要](PROJECT_SUMMARY.md)

