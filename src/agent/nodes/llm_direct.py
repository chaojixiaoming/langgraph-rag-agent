from typing import Dict, Any
from langgraph.runtime import Runtime
from ..state import State
from ..context import Context
from ..config import config


def _safe_get_context(runtime):
    """安全获取 runtime.context"""
    try:
        if runtime and hasattr(runtime, 'context') and runtime.context:
            return runtime.context
    except:
        pass
    return {}


async def llm_direct_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """LLM直接回答节点：不需要工具时直接生成回答"""
    from langchain_openai import ChatOpenAI
    
    context = _safe_get_context(runtime)
    
    model_name = context.get("model_name") if context else config._config["model"]["name"]
    temperature = context.get("temperature") if context else config._config["model"]["temperature"]
    
    model_config = config.model_config
    
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=model_config.get("api_key"),
        base_url=model_config.get("api_base")
    )
    
    user_input = state.user_input
    messages = [{"role": "user", "content": user_input}]
    
    response = await llm.ainvoke(messages)
    
    print(f"[LLM Direct] 使用模型: {model_name}")
    print(f"[LLM Direct] 生成回答: {response.content[:100]}...")
    
    return {
        "final_response": response.content,
        "messages": [{"role": "assistant", "content": response.content}]
    }
