"""
Learner - 智能学习管理系统
快速启动脚本
"""
import os
import sys
import subprocess


def check_requirements():
    """检查必要的依赖"""
    requirements = {
        'docker': 'Docker',
        'docker-compose': 'Docker Compose'
    }
    
    missing = []
    for cmd, name in requirements.items():
        if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
            missing.append(name)
    
    return missing


def main():
    """主函数"""
    print("=" * 60)
    print("🎓 Learner - 智能学习管理系统")
    print("=" * 60)
    print()
    
    # 检查依赖
    missing = check_requirements()
    if missing:
        print("❌ 缺少以下依赖:")
        for dep in missing:
            print(f"   - {dep}")
        print()
        print("请先安装所需依赖，然后重试。")
        print("详细安装说明请查看: SETUP.md")
        sys.exit(1)
    
    # 检查环境变量文件
    if not os.path.exists('.env'):
        print("⚠️  未找到 .env 文件")
        print()
        if os.path.exists('.env.example'):
            response = input("是否从 .env.example 创建 .env 文件？(y/n): ")
            if response.lower() == 'y':
                os.system('cp .env.example .env')
                print("✅ .env 文件已创建")
                print()
                print("📝 请编辑 .env 文件，配置 Azure OpenAI 信息:")
                print("   nano .env  # 或使用其他编辑器")
                print()
                print("配置完成后，再次运行此脚本启动服务。")
                sys.exit(0)
        else:
            print("请创建 .env 文件并配置必要的环境变量。")
            print("详细说明请查看: SETUP.md")
            sys.exit(1)
    
    print("🚀 启动服务...")
    print()
    
    # 启动 Docker Compose
    try:
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        print()
        print("=" * 60)
        print("✅ 服务启动成功！")
        print("=" * 60)
        print()
        print("📱 前端地址: http://localhost:3000")
        print("🔧 后端地址: http://localhost:8000")
        print("📖 API 文档: http://localhost:8000/api/docs")
        print()
        print("💡 查看日志: docker-compose logs -f")
        print("🛑 停止服务: docker-compose down")
        print()
        print("=" * 60)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
