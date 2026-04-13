import pytest
from src.agent.graph import agent, build_graph, route_decision
from src.agent.state import State


class TestGraphBuilding:
    """测试图构建"""
    
    def test_build_graph(self):
        """测试图构建成功"""
        graph = build_graph()
        assert graph is not None
    
    def test_agent_exists(self):
        """测试 agent 实例存在"""
        assert agent is not None


class TestRouteDecision:
    """测试路由决策函数"""
    
    def test_route_direct_llm(self):
        """测试直接 LLM 路由"""
        state = State(route_decision="direct_llm")
        result = route_decision(state)
        assert result == "direct_llm"
    
    def test_route_need_tools(self):
        """测试需要工具路由"""
        state = State(route_decision="need_tools")
        result = route_decision(state)
        assert result == "need_tools"
    
    def test_route_need_rag(self):
        """测试需要 RAG 路由"""
        state = State(route_decision="need_rag")
        result = route_decision(state)
        assert result == "need_rag"


class TestGraphStructure:
    """测试图结构完整性"""
    
    def test_graph_nodes_exist(self):
        """测试图包含所有必要节点"""
        graph = build_graph()
        
        nodes = list(graph.nodes.keys())
        expected_nodes = [
            "router",
            "llm_direct", 
            "tool_executor",
            "result_formatter",
            "response_generator",
            "memory_saver"
        ]
        
        for node in expected_nodes:
            assert node in nodes, f"缺少节点: {node}"
