#!/usr/bin/env python3
"""
验证 Runtime 导入是否正确

使用方法:
    python scripts/verify_imports.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_runtime_import():
    """测试 Runtime 导入"""
    print("=" * 60)
    print("🔍 验证 LangGraph Runtime 导入")
    print("=" * 60)
    
    try:
        print("\n1. 测试从 langgraph.runtime 导入 Runtime...")
        from langgraph.runtime import Runtime
        print("   ✅ 成功: from langgraph.runtime import Runtime")
        
        print("\n2. 测试 Runtime 类型...")
        print(f"   ✅ Runtime 类型: {Runtime}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ 失败: {e}")
        
        print("\n3. 尝试备选方案...")
        try:
            from langgraph.types import runtime
            print(f"   ⚠️ 备选方案: from langgraph.types import runtime")
            print(f"   ℹ️ runtime 对象: {runtime}")
            return True
        except ImportError as e2:
            print(f"   ❌ 备选方案也失败: {e2}")
            return False


def test_node_imports():
    """测试所有节点的导入"""
    print("\n" + "=" * 60)
    print("🔍 验证所有节点模块导入")
    print("=" * 60)
    
    nodes = [
        ("router", "src.agent.nodes.router"),
        ("llm_direct", "src.agent.nodes.llm_direct"),
        ("tool_executor", "src.agent.nodes.tool_executor"),
        ("result_formatter", "src.agent.nodes.result_formatter"),
        ("response_generator", "src.agent.nodes.response_generator"),
        ("memory_saver", "src.agent.nodes.memory_saver"),
    ]
    
    all_success = True
    
    for name, module_path in nodes:
        try:
            __import__(module_path)
            print(f"\n✅ {name}: 导入成功")
        except Exception as e:
            print(f"\n❌ {name}: 导入失败 - {e}")
            all_success = False
    
    return all_success


def test_graph_import():
    """测试图构建导入"""
    print("\n" + "=" * 60)
    print("🔍 验证图构建")
    print("=" * 60)
    
    try:
        from src.agent.graph import agent, build_graph
        print("\n✅ 图构建成功")
        print(f"   Agent 实例: {agent}")
        return True
    except Exception as e:
        print(f"\n❌ 图构建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "🚀" * 30)
    print("LangGraph Agent 导入验证工具")
    print("🚀" * 30 + "\n")
    
    results = []
    
    results.append(("Runtime 导入", test_runtime_import()))
    results.append(("节点模块导入", test_node_imports()))
    results.append(("图构建", test_graph_import()))
    
    print("\n" + "=" * 60)
    print("📊 验证结果总结")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} - {name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n🎉 所有验证通过！项目可以正常运行。")
        print("\n下一步:")
        print("  1. 运行: python scripts/init_vector_db.py")
        print("  2. 启动: python main.py")
        return 0
    else:
        print("\n⚠️ 部分验证未通过，请检查错误信息。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
