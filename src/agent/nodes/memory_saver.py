from typing import Dict, Any
from langgraph.runtime import Runtime
from ..state import State
from ..context import Context
from ..utils.memory import create_memory_manager


def _safe_get_context(runtime):
    """安全获取 runtime.context"""
    try:
        if runtime and hasattr(runtime, 'context') and runtime.context:
            return runtime.context
    except:
        pass
    return {}


async def memory_saver_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """保存记忆节点：将对话和结果保存到记忆系统"""
    context = _safe_get_context(runtime)
    
    memory_enabled = context.get("memory_enabled") if context else True
    
    if not memory_enabled:
        print("[Memory Saver] 记忆功能已禁用")
        return {}
    
    memory_manager = create_memory_manager()
    
    session_id = f"session_{hash(state.user_input) % 10000}"
    
    memory_data = {
        "user_input": state.user_input,
        "response": state.final_response,
        "route_decision": state.route_decision,
        "tool_used": len(state.tool_results) > 0,
        "rag_used": len(state.rag_results) > 0
    }
    
    success = memory_manager.save_memory(session_id, memory_data)
    
    if success:
        print(f"[Memory Saver] 记忆保存成功 - Session: {session_id}")
        return {
            "memory_data": memory_data
        }
    else:
        print("[Memory Saver] 记忆保存失败")
        return {}
