#!/bin/bash

# 启动开发环境脚本

echo "🚀 启动 Learner 开发环境..."

# 检查是否安装了 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查是否存在 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，从 .env.example 复制..."
    cp .env.example .env
    echo "✅ 请编辑 .env 文件配置 Azure OpenAI 信息"
    exit 1
fi

# 启动 Docker Compose
echo "📦 启动 Docker 容器..."
docker-compose up -d

echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo "📖 API 文档: http://localhost:8000/api/docs"
echo ""
echo "💡 使用 'docker-compose logs -f' 查看日志"
echo "🛑 使用 'docker-compose down' 停止服务"

