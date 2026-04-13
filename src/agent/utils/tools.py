from langchain_core.tools import tool
from typing import Dict, Any


@tool
def search_web(query: str) -> str:
    """搜索网络获取信息"""
    return f"搜索结果: 关于 '{query}' 的相关信息..."


@tool
def calculator(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city}的天气: 晴天, 25°C"


TOOLS = [search_web, calculator, get_weather]


def get_tools_by_name(tool_names: list) -> list:
    """根据名称获取工具列表"""
    tool_map = {tool.name: tool for tool in TOOLS}
    return [tool_map[name] for name in tool_names if name in tool_map]
