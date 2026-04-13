from typing import Dict, Any
from langgraph.runtime import Runtime
from ..state import State
from ..context import Context
from ..config import config


async def router_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """路由判断节点：决定是否需要调用工具或使用 RAG"""
    user_input = state.user_input or (state.messages[-1].content if state.messages else "")
    
    # 安全获取 context，如果为 None 则使用默认配置
    try:
        context = runtime.context if runtime and hasattr(runtime, 'context') and runtime.context else {}
    except:
        context = {}
    
    use_tools = context.get("use_tools") if context else config._config["tools"]["enabled"]
    use_rag = context.get("use_rag") if context else config._config["rag"]["enabled"]
    
    agent_config = config.agent_config
    keywords_need_tools = agent_config.get(
        "route_keywords_tools",
        ["搜索", "计算", "天气", "查询"]
    )
    keywords_need_rag = agent_config.get(
        "route_keywords_rag",
        ["什么是", "如何", "介绍", "文档"]
    )
    
    needs_tools = any(kw in user_input for kw in keywords_need_tools) and use_tools
    needs_rag = any(kw in user_input for kw in keywords_need_rag) and use_rag
    
    if needs_tools or needs_rag:
        route_decision = "need_tools"
        if needs_rag:
            route_decision = "need_rag"
    else:
        route_decision = "direct_llm"
    
    print(f"[Router] 用户输入: {user_input[:50]}...")
    print(f"[Router] 路由决策: {route_decision}")
    
    return {
        "route_decision": route_decision,
        "user_input": user_input
    }
