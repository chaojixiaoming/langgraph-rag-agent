#!/usr/bin/env python3
"""
路径配置验证工具

使用方法:
    python scripts/verify_paths.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_config_path():
    """测试 config.yaml 路径"""
    print("=" * 60)
    print("🔍 验证配置文件路径")
    print("=" * 60)
    
    try:
        from src.agent.config import config
        
        print(f"\n✅ config.yaml 加载成功!")
        print(f"   项目根目录: {Path(__file__).parent.parent}")
        
        # 测试配置读取
        model_name = config._config.get("model", {}).get("name", "未知")
        print(f"   模型名称: {model_name}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ 配置文件未找到: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 配置加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_env_file():
    """测试 .env 文件路径"""
    print("\n" + "=" * 60)
    print("🔍 验证环境变量文件")
    print("=" * 60)
    
    import os
    
    env_path = Path(__file__).parent.parent / ".env"
    
    if env_path.exists():
        print(f"\n✅ .env 文件存在: {env_path}")
        
        # 检查关键环境变量
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        api_base = os.getenv("DEEPSEEK_API_BASE", "")
        
        if api_key and "your_" not in api_key.lower():
            print(f"   DEEPSEEK_API_KEY: {'*' * 8}...{api_key[-4:]} (已配置)")
        else:
            print(f"   ⚠️ DEEPSEEK_API_KEY: 未配置或使用默认值")
        
        print(f"   DEEPSEEK_API_BASE: {api_base}")
        
        return True
    else:
        print(f"\n❌ .env 文件不存在: {env_path}")
        return False


def test_knowledge_base():
    """测试知识库文件路径"""
    print("\n" + "=" * 60)
    print("🔍 验证知识库文件")
    print("=" * 60)
    
    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base.txt"
    
    if kb_path.exists():
        size_kb = kb_path.stat().st_size / 1024
        print(f"\n✅ 知识库文件存在: {kb_path}")
        print(f"   文件大小: {size_kb:.2f} KB")
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   总行数: {len(lines)} 行")
            print(f"   前3行预览:")
            for i, line in enumerate(lines[:3], 1):
                print(f"      {i}: {line.strip()[:50]}...")
        
        return True
    else:
        print(f"\n❌ 知识库文件不存在: {kb_path}")
        return False


def test_vector_db_dir():
    """测试向量数据库目录"""
    print("\n" + "=" * 60)
    print("🔍 验证向量数据库目录")
    print("=" * 60)
    
    from src.agent.config import config
    
    vector_db_dir = Path(config.rag_config.get("persist_directory", "./vector_db"))
    
    if vector_db_dir.exists():
        files = list(vector_db_dir.glob("*"))
        print(f"\n✅ 向量数据库目录已初始化: {vector_db_dir}")
        print(f"   包含文件: {len(files)} 个")
        return True
    else:
        print(f"\n⚠️ 向量数据库目录尚未创建: {vector_db_dir}")
        print(f"   提示: 运行 'python scripts/init_vector_db.py' 初始化")
        return True  # 这不是错误，只是需要初始化


def main():
    """主函数"""
    print("\n" + "🗺️" * 30)
    print("LangGraph Agent 路径配置验证工具")
    print("🗺️" * 30 + "\n")
    
    results = []
    
    results.append(("config.yaml 路径", test_config_path()))
    results.append((".env 文件路径", test_env_file()))
    results.append(("知识库文件路径", test_knowledge_base()))
    results.append(("向量数据库目录", test_vector_db_dir()))
    
    print("\n" + "=" * 60)
    print("📊 验证结果总结")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} - {name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n🎉 所有路径配置正确！")
        print("\n下一步操作:")
        print("  1. 如果向量数据库未初始化，运行:")
        print("     python scripts/init_vector_db.py")
        print("  2. 启动 Agent:")
        print("     python main.py")
        return 0
    else:
        print("\n⚠️ 部分路径配置有问题，请检查上方错误信息。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
