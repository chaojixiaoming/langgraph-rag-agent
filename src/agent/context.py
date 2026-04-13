from typing import TypedDict, Optional


class Context(TypedDict):
    model_name: str
    temperature: float
    max_tokens: int
    use_rag: bool
    use_tools: bool
    rag_config: Optional[dict]
    memory_enabled: bool
