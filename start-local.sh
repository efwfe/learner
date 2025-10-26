#!/bin/bash

# 本地开发启动脚本（不使用 Docker）

echo "🚀 启动 Learner 本地开发环境..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

# 启动后端
echo "🔧 启动后端服务..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# 启动后端（后台运行）
python -m app.main &
BACKEND_PID=$!
echo "✅ 后端启动成功 (PID: $BACKEND_PID)"

cd ..

# 启动前端
echo "🎨 启动前端服务..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
echo "✅ 前端启动成功 (PID: $FRONTEND_PID)"

cd ..

echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo "📖 API 文档: http://localhost:8000/api/docs"
echo ""
echo "💡 按 Ctrl+C 停止服务"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

