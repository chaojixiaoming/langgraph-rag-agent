from dataclasses import dataclass, field
from typing import Annotated
from langgraph.graph.message import add_messages


@dataclass
class State:
    messages: Annotated[list, add_messages] = field(default_factory=list)
    user_input: str = ""
    route_decision: str = ""
    tool_calls: list = field(default_factory=list)
    tool_results: list = field(default_factory=list)
    rag_results: list = field(default_factory=list)
    formatted_results: str = ""
    final_response: str = ""
    memory_data: dict = field(default_factory=dict)
