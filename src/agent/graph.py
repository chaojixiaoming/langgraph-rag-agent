import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from langgraph.graph import StateGraph, START, END
from src.agent.state import State
from src.agent.context import Context
from src.agent.nodes.router import router_node
from src.agent.nodes.llm_direct import llm_direct_node
from src.agent.nodes.tool_executor import tool_executor_node
from src.agent.nodes.result_formatter import result_formatter_node
from src.agent.nodes.response_generator import response_generator_node
from src.agent.nodes.memory_saver import memory_saver_node


def route_decision(state: State) -> str:
    """条件路由函数：根据路由决策决定下一步"""
    return state.route_decision


def build_graph():
    """构建 LangGraph 工作流图"""
    
    graph = StateGraph(State, context_schema=Context)
    
    graph.add_node("router", router_node)
    graph.add_node("llm_direct", llm_direct_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("result_formatter", result_formatter_node)
    graph.add_node("response_generator", response_generator_node)
    graph.add_node("memory_saver", memory_saver_node)
    
    graph.add_edge(START, "router")
    
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "direct_llm": "llm_direct",
            "need_tools": "tool_executor",
            "need_rag": "tool_executor"
        }
    )
    
    graph.add_edge("llm_direct", "response_generator")
    graph.add_edge("tool_executor", "result_formatter")
    graph.add_edge("result_formatter", "response_generator")
    graph.add_edge("response_generator", "memory_saver")
    graph.add_edge("memory_saver", END)
    
    agent = graph.compile(name="Agent Workflow")
    
    return agent


agent = build_graph()


if __name__ == "__main__":
    import asyncio
    
    async def main():
        config = {
            "configurable": {
                "model_name": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
                "use_rag": True,
                "use_tools": True,
                "rag_config": {},
                "memory_enabled": True
            }
        }
        
        test_inputs = [
            {"user_input": "你好，请介绍一下你自己"},
            {"user_input": "帮我计算 123 * 456"},
            {"user_input": "什么是LangGraph？"}
        ]
        
        for input_data in test_inputs:
            print(f"\n{'='*60}")
            print(f"用户输入: {input_data['user_input']}")
            print('='*60)
            
            result = await agent.ainvoke(input_data, config=config)
            
            print(f"\n最终回答: {result['final_response']}")
            print(f"路由决策: {result['route_decision']}")
    
    asyncio.run(main())
