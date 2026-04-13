#!/usr/bin/env python3
"""
初始化知识库向量数据库

使用方法:
    python scripts/init_vector_db.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.utils.vector_db import initialize_knowledge_base
from src.agent.config import config


def main():
    """初始化向量数据库"""
    print("=" * 60)
    print("🚀 初始化 LangGraph 知识库向量数据库")
    print("=" * 60)
    
    print("\n📋 配置信息:")
    rag_config = config.rag_config
    print(f"   - Embedding 模型: {rag_config.get('embedding_model', 'BAAI/bge-small-zh-v1.5')}")
    print(f"   - 分块大小: {rag_config.get('chunk_size', 500)}")
    print(f"   - 重叠大小: {rag_config.get('chunk_overlap', 50)}")
    print(f"   - 存储路径: {rag_config.get('persist_directory', './vector_db')}")
    
    knowledge_file = Path(__file__).parent.parent / "data" / "knowledge_base.txt"
    
    if not knowledge_file.exists():
        print(f"\n❌ 知识库文件不存在: {knowledge_file}")
        return 1
    
    print(f"\n📚 知识库文件: {knowledge_file}")
    print(f"   文件大小: {knowledge_file.stat().st_size / 1024:.2f} KB")
    
    try:
        manager = initialize_knowledge_base(str(knowledge_file))
        
        print("\n✅ 向量数据库初始化成功!")
        print("\n📊 统计信息:")
        print(f"   - 向量存储路径: {rag_config.get('persist_directory', './vector_db')}")
        print(f"   - Embedding 模型已加载")
        print(f"   - 知识库已向量化并持久化")
        
        print("\n💡 提示:")
        print("   - 可以通过 RAG 系统进行语义检索")
        print("   - 运行 'python main.py' 启动 Agent 进行测试")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 初始化失败!")
        print(f"错误详情: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
