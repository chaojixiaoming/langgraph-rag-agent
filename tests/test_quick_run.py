#!/usr/bin/env python3
"""
快速测试脚本 - 用于验证 Agent 工作流的基本功能

使用方法:
    python tests/test_quick_run.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.graph import agent
from src.agent.utils.tools import TOOLS
from src.agent.utils.rag import create_rag_retriever
from src.agent.utils.memory import create_memory_manager


def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print('='*60)


async def test_basic_components():
    """测试基本组件"""
    print_separator("1. 测试基本组件")
    
    print("\n✅ 工具列表:")
    for tool in TOOLS:
        print(f"   - {tool.name}: {tool.description}")
    
    retriever = create_rag_retriever()
    results = await retriever.retrieve("LangGraph", top_k=2)
    print(f"\n✅ RAG 检索器: 找到 {len(results)} 条结果")
    
    memory_mgr = create_memory_manager()
    success = memory_mgr.save_memory("test_session", {"test": "data"})
    print(f"✅ 记忆管理器: 保存{'成功' if success else '失败'}")


async def test_router_scenarios():
    """测试路由场景"""
    print_separator("2. 测试路由决策场景")
    
    config = {
        "configurable": {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000,
            "use_rag": True,
            "use_tools": True,
            "rag_config": {},
            "memory_enabled": True
        }
    }
    
    test_cases = [
        ("你好，介绍一下自己", "direct_llm"),
        ("帮我计算 123*456", "need_tools"),
        ("什么是LangGraph？", "need_rag"),
        ("今天天气怎么样", "need_tools"),
    ]
    
    for user_input, expected_route in test_cases:
        try:
            result = await agent.ainvoke(
                {"user_input": user_input},
                config=config
            )
            actual_route = result.get("route_decision", "unknown")
            status = "✅" if actual_route == expected_route else "⚠️"
            print(f"{status} 输入: {user_input[:30]}...")
            print(f"   预期路由: {expected_route}, 实际: {actual_route}")
        except Exception as e:
            print(f"❌ 测试失败: {user_input[:30]}...")
            print(f"   错误: {str(e)}")


async def test_full_workflow():
    """测试完整工作流"""
    print_separator("3. 测试完整工作流")
    
    config = {
        "configurable": {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 500,
            "use_rag": True,
            "use_tools": True,
            "rag_config": {},
            "memory_enabled": True
        }
    }
    
    test_input = "用一句话介绍 LangGraph"
    
    print(f"\n📝 用户输入: {test_input}")
    print("-" * 40)
    
    try:
        result = await agent.ainvoke({"user_input": test_input}, config=config)
        
        print(f"\n🎯 路由决策: {result.get('route_decision')}")
        print(f"🔧 使用工具: {len(result.get('tool_results', []))} 个")
        print(f"📚 RAG 结果: {len(result.get('rag_results', []))} 条")
        print(f"\n💬 最终回答:")
        print(f"   {result.get('final_response', '无回答')[:200]}...")
        print(f"\n✅ 工作流执行成功!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败!")
        print(f"错误详情: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 LangGraph Agent 快速测试")
    print("="*60)
    
    print("\n📦 项目结构检查:")
    print(f"   - pyproject.toml: {'✅' if Path('pyproject.toml').exists() else '❌'}")
    print(f"   - langgraph.json: {'✅' if Path('langgraph.json').exists() else '❌'}")
    print(f"   - src/agent/: {'✅' if Path('src/agent').exists() else '❌'}")
    print(f"   - tests/: {'✅' if Path('tests').exists() else '❌'}")
    
    await test_basic_components()
    await test_router_scenarios()
    success = await test_full_workflow()
    
    print_separator("测试总结")
    
    if success:
        print("\n🎉 所有核心测试通过!")
        print("\n下一步操作:")
        print("  1. 配置 .env 文件中的 OPENAI_API_KEY")
        print("  2. 运行: pip install -e .")
        print("  3. 运行: python main.py 开始交互模式")
        print("  4. 或运行: pytest tests/ 进行完整测试")
    else:
        print("\n⚠️ 部分测试未通过，请检查配置和依赖")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
