from typing import Dict, Any
from langgraph.runtime import Runtime
from src.agent.state import State
from src.agent.context import Context
from src.agent.config import config
from src.agent.utils.tools import TOOLS, get_tools_by_name
from src.agent.utils.rag import create_rag_retriever


def _safe_get_context(runtime):
    """安全获取 runtime.context"""
    try:
        if runtime and hasattr(runtime, 'context') and runtime.context:
            return runtime.context
    except:
        pass
    return {}


async def tool_executor_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """工具执行/RAG检索节点：执行工具调用或RAG检索"""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    
    context = _safe_get_context(runtime)
    route_decision = state.route_decision
    user_input = state.user_input
    tool_results = []
    rag_results = []
    
    model_config = config.model_config
    model_name = context.get("model_name") if context else config._config["model"]["name"]
    
    if route_decision == "need_tools":
        print(f"[Tool Executor] 执行工具调用...")
        
        llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=model_config.get("api_key"),
            base_url=model_config.get("api_base")
        )
        
        llm_with_tools = llm.bind_tools(TOOLS)
        
        response = await llm_with_tools.ainvoke([HumanMessage(content=user_input)])
        
        if response.tool_calls:
            state["tool_calls"] = response.tool_calls
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                tool_map = {tool.name: tool for tool in TOOLS}
                if tool_name in tool_map:
                    tool = tool_map[tool_name]
                    result = tool.invoke(tool_args)
                    tool_results.append({
                        "tool_name": tool_name,
                        "arguments": tool_args,
                        "result": result
                    })
                    print(f"[Tool Executor] 工具 {tool_name} 执行完成")
    
    elif route_decision == "need_rag":
        print(f"[Tool Executor] 执行 RAG 检索...")
        
        rag_config = context.get("rag_config") if context else {}
        retriever = create_rag_retriever(rag_config)
        
        rag_results = await retriever.retrieve(user_input)
        state["rag_results"] = rag_results
        
        print(f"[Tool Executor] RAG 检索到 {len(rag_results)} 条结果")
    
    return {
        "tool_results": tool_results,
        "rag_results": rag_results
    }
