from typing import Dict, Any
from langgraph.runtime import Runtime
from src.agent.state import State
from src.agent.context import Context
from src.agent.config import config


def _safe_get_context(runtime):
    """安全获取 runtime.context"""
    try:
        if runtime and hasattr(runtime, 'context') and runtime.context:
            return runtime.context
    except:
        pass
    return {}


async def response_generator_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """最终回答生成节点：基于整理后的结果或LLM直接回答生成最终响应"""
    from langchain_openai import ChatOpenAI
    
    context = _safe_get_context(runtime)
    
    model_name = context.get("model_name") if context else config._config["model"]["name"]
    temperature = context.get("temperature") if context else config._config["model"]["temperature"]
    max_tokens = context.get("max_tokens") if context else config._config["model"]["max_tokens"]
    
    model_config = config.model_config
    
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=model_config.get("api_key"),
        base_url=model_config.get("api_base")
    )
    
    user_input = state.user_input
    
    if state.formatted_results:
        prompt = f"""基于以下信息回答用户问题：

用户问题: {user_input}

参考信息:
{state.formatted_results}

请根据以上信息给出详细、准确的回答。如果参考信息不足，请基于你的知识进行补充。"""
    else:
        prompt = user_input
    
    messages = [{"role": "user", "content": prompt}]
    response = await llm.ainvoke(messages)
    
    final_response = response.content
    
    print(f"[Response Generator] 使用模型: {model_name}")
    print(f"[Response Generator] 生成最终回答: {final_response[:100]}...")
    
    return {
        "final_response": final_response,
        "messages": [{"role": "assistant", "content": final_response}]
    }
