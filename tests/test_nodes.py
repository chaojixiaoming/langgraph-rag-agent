import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.agent.state import State
from src.agent.context import Context
from src.agent.nodes.router import router_node
from src.agent.nodes.llm_direct import llm_direct_node
from src.agent.nodes.tool_executor import tool_executor_node
from src.agent.nodes.result_formatter import result_formatter_node
from src.agent.nodes.response_generator import response_generator_node
from src.agent.nodes.memory_saver import memory_saver_node
from langgraph.runtime import Runtime


class TestRouterNode:
    """测试路由节点"""
    
    @pytest.mark.asyncio
    async def test_route_to_direct_llm(self):
        """测试路由到 LLM 直接回答"""
        state = State(user_input="你好，请介绍一下你自己")
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "use_tools": True,
            "use_rag": True,
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await router_node(state, runtime)
        
        assert result["route_decision"] == "direct_llm"
        assert result["user_input"] == "你好，请介绍一下你自己"
    
    @pytest.mark.asyncio
    async def test_route_to_need_tools(self):
        """测试路由到工具调用"""
        state = State(user_input="帮我计算 123 * 456")
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "use_tools": True,
            "use_rag": True,
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await router_node(state, runtime)
        
        assert result["route_decision"] == "need_tools"
    
    @pytest.mark.asyncio
    async def test_route_to_need_rag(self):
        """测试路由到 RAG 检索"""
        state = State(user_input="什么是LangGraph？")
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "use_tools": True,
            "use_rag": True,
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await router_node(state, runtime)
        
        assert result["route_decision"] == "need_rag"


class TestToolExecutorNode:
    """测试工具执行节点"""
    
    @pytest.mark.asyncio
    async def test_execute_tools(self):
        """测试工具执行"""
        state = State(
            user_input="帮我计算 123 + 456",
            route_decision="need_tools"
        )
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "use_tools": True,
            "use_rag": True,
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "rag_config": {},
            "memory_enabled": True
        }
        
        with patch('src.agent.nodes.tool_executor.ChatOpenAI') as mock_llm:
            mock_response = Mock()
            mock_response.tool_calls = [
                {
                    "name": "calculator",
                    "args": {"expression": "123 + 456"},
                    "id": "call_123"
                }
            ]
            mock_llm.return_value.bind_tools.return_value.ainvoke = AsyncMock(return_value=mock_response)
            
            result = await tool_executor_node(state, runtime)
            
            assert "tool_results" in result
            assert len(result["tool_results"]) > 0
    
    @pytest.mark.asyncio
    async def test_execute_rag(self):
        """测试 RAG 执行"""
        state = State(
            user_input="什么是 LangGraph?",
            route_decision="need_rag"
        )
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "use_tools": False,
            "use_rag": True,
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await tool_executor_node(state, runtime)
        
        assert "rag_results" in result
        assert len(result["rag_results"]) > 0


class TestResultFormatterNode:
    """测试结果整理节点"""
    
    @pytest.mark.asyncio
    async def test_format_tool_results(self):
        """测试格式化工具结果"""
        state = State(
            tool_results=[
                {
                    "tool_name": "calculator",
                    "arguments": {"expression": "123+456"},
                    "result": "579"
                }
            ]
        )
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "use_rag": True,
            "use_tools": True,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await result_formatter_node(state, runtime)
        
        assert "formatted_results" in result
        assert "calculator" in result["formatted_results"]
        assert "579" in result["formatted_results"]
    
    @pytest.mark.asyncio
    async def test_format_rag_results(self):
        """测试格式化 RAG 结果"""
        state = State(
            rag_results=[
                {"content": "LangGraph 是一个库", "score": 0.9, "source": "kb"}
            ]
        )
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "use_rag": True,
            "use_tools": True,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await result_formatter_node(state, runtime)
        
        assert "formatted_results" in result
        assert "RAG" in result["formatted_results"]
        assert "LangGraph" in result["formatted_results"]


class TestMemorySaverNode:
    """测试记忆保存节点"""
    
    @pytest.mark.asyncio
    async def test_save_memory_success(self):
        """测试成功保存记忆"""
        state = State(
            user_input="测试输入",
            final_response="测试回答",
            route_decision="direct_llm"
        )
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "use_rag": True,
            "use_tools": True,
            "rag_config": {},
            "memory_enabled": True
        }
        
        result = await memory_saver_node(state, runtime)
        
        assert "memory_data" in result
        assert result["memory_data"]["user_input"] == "测试输入"
        assert result["memory_data"]["response"] == "测试回答"
    
    @pytest.mark.asyncio
    async def test_memory_disabled(self):
        """测试记忆功能禁用"""
        state = State(user_input="测试")
        runtime = Mock(spec=Runtime)
        runtime.context = {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "use_rag": True,
            "use_tools": True,
            "rag_config": {},
            "memory_enabled": False
        }
        
        result = await memory_saver_node(state, runtime)
        
        assert result == {}
