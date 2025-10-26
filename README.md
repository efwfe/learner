# Learner - Intelligent Learning Management System

[English](#english) | [中文](README.zh-CN.md)

<a name="english"></a>

A personal knowledge management platform based on the forgetting curve with spaced repetition and AI-powered features.

## ✨ Features

- 📝 **Learning Content Management** - Record daily learning with AI knowledge extraction
- 📊 **Intelligent Review System** - Based on **SuperMemo SM-2** algorithm for spaced repetition
- 🕸️ **Knowledge Graph** - Visualize relationships between knowledge points
- 🤖 **AI-Powered** - Auto-generate summaries and relationship suggestions

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone and configure
git clone <repository-url>
cd learner
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Start services
docker-compose up -d
```

**Access:** http://localhost:3000

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Azure OpenAI, SQLite
- **Frontend**: React 18, TypeScript, Vite, Zustand, i18next
- **Deployment**: Docker, Docker Compose

## 📖 Usage

1. **Configure Azure OpenAI** in `.env` file
2. **Add Knowledge** - Visit Knowledge Base page to create knowledge points
3. **Start Review** - Follow SM-2 algorithm-based review plan
4. **Explore Graph** - Visualize knowledge relationships

## 🌐 Internationalization

The application supports both English and Chinese. Use the language switcher in the top-right corner to change languages.

## 📋 API Documentation

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

---

💡 **For detailed documentation:**
- [Quick Start Guide](QUICKSTART.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Project Summary](PROJECT_SUMMARY.md)
