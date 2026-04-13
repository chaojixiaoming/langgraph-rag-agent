"""
验证导入修复 - 测试所有模块是否能正确加载
运行方式: python scripts/verify_imports.py
"""

import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("[VERIFY] LangGraph Project Import Verification")
print("=" * 60)
print(f"[INFO] Project Root: {project_root}")
print()

errors = []
successes = []

def test_import(module_path, description):
    """测试单个模块导入"""
    try:
        __import__(module_path)
        successes.append((module_path, description))
        print(f"[OK] {description}")
        return True
    except Exception as e:
        errors.append((module_path, description, str(e)))
        print(f"[FAIL] {description}")
        print(f"      Error: {e}")
        return False


print("\n[MODULES] Core Modules:")
print("-" * 40)

test_import("src.agent.state", "State Definition")
test_import("src.agent.context", "Context Definition")
test_import("src.agent.config", "Config Manager")

print("\n[MODULES] Utility Modules:")
print("-" * 40)

test_import("src.agent.utils.tools", "Tools Definition")
test_import("src.agent.utils.memory", "Memory Manager")

print("\n[MODULES] Node Modules:")
print("-" * 40)

test_import("src.agent.nodes.router", "Router Node")
test_import("src.agent.nodes.llm_direct", "LLM Direct Node")
test_import("src.agent.nodes.tool_executor", "Tool Executor Node")
test_import("src.agent.nodes.result_formatter", "Result Formatter Node")
test_import("src.agent.nodes.response_generator", "Response Generator Node")
test_import("src.agent.nodes.memory_saver", "Memory Saver Node")

print("\n[MODULES] Main Graph Module:")
print("-" * 40)

test_import("src.agent.graph", "Graph Construction (IMPORTANT!)")

print("\n" + "=" * 60)
print(f"[RESULT] {len(successes)} passed, {len(errors)} failed")
print("=" * 60)

if errors:
    print("\n[ERROR] Failed modules:")
    for module_path, desc, error in errors:
        print(f"   - {desc}: {error}")
    sys.exit(1)
else:
    print("\n[SUCCESS] All imports successful!")
    print("\n[NEXT STEPS]")
    print("   1. Install dependencies: pip install -e . OR uv sync")
    print("   2. Install LangGraph CLI: pip install 'langgraph[cli]'")
    print("   3. Run dev server: langgraph dev")
    print()
    print("[TIP] If 'langgraph' command not found:")
    print("   pip install 'langgraph[cli]'")
    print("   OR")
    print("   uv pip install 'langgraph[cli]'")
    sys.exit(0)
