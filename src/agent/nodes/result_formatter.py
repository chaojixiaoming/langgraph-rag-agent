from typing import Dict, Any
from langgraph.runtime import Runtime
from src.agent.state import State
from src.agent.context import Context
from src.agent.utils.rag import create_rag_retriever


def _safe_get_context(runtime):
    """安全获取 runtime.context"""
    try:
        if runtime and hasattr(runtime, 'context') and runtime.context:
            return runtime.context
    except:
        pass
    return {}


async def result_formatter_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """结果整理节点：将工具执行结果或RAG结果整理成结构化格式"""
    formatted_parts = []
    
    if state.tool_results:
        formatted_parts.append("=== 工具执行结果 ===")
        for i, result in enumerate(state.tool_results, 1):
            formatted_parts.append(
                f"\n工具{i}: {result['tool_name']}\n"
                f"参数: {result['arguments']}\n"
                f"结果: {result['result']}"
            )
    
    if state.rag_results:
        context = _safe_get_context(runtime)
        rag_config = context.get("rag_config") if context else {}
        retriever = create_rag_retriever(rag_config)
        
        formatted_parts.append("\n=== RAG 检索结果 ===")
        formatted_text = retriever.format_results(state.rag_results)
        formatted_parts.append(formatted_text)
    
    formatted_results = "\n".join(formatted_parts)
    
    print(f"[Result Formatter] 整理完成，结果长度: {len(formatted_results)}")
    
    return {
        "formatted_results": formatted_results
    }
