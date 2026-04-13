from typing import List, Dict, Any, Optional
from .vector_db import VectorDBManager, initialize_knowledge_base


class RAGRetriever:
    """RAG 检索器 - 基于向量数据库"""
    
    _vector_db_manager: Optional[VectorDBManager] = None
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self._ensure_vector_db_initialized()
    
    @classmethod
    def _ensure_vector_db_initialized(cls):
        """确保向量数据库已初始化（单例模式）"""
        if cls._vector_db_manager is None:
            try:
                cls._vector_db_manager = initialize_knowledge_base()
            except Exception as e:
                print(f"[RAG] 向量数据库初始化失败: {e}")
                print("[RAG] 使用备用检索模式")
                cls._vector_db_manager = None
    
    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """检索相关文档"""
        top_k = self.config.get("top_k", top_k)
        
        if self._vector_db_manager is None:
            return await self._fallback_retrieve(query, top_k)
        
        try:
            results = self._vector_db_manager.retrieve(query, top_k=top_k)
            
            print(f"[RAG] 从向量库检索到 {len(results)} 条结果")
            
            return results
            
        except Exception as e:
            print(f"[RAG] 向量检索失败: {e}")
            return await self._fallback_retrieve(query, top_k)
    
    async def _fallback_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """备用检索方案（当向量数据库不可用时）"""
        fallback_docs = [
            "LangGraph 是 LangChain 生态系统中用于构建有状态、多步骤 AI 应用的核心框架。",
            "StateGraph 是 LangGraph 的核心组件，用于构建状态图，支持节点、边和条件路由。",
            "LangGraph 支持 RAG（检索增强生成）集成，可以结合向量数据库实现知识问答。",
            "DeepSeek 是高性能的大语言模型系列，适合中文场景的智能应用开发。",
            "FAISS 是 Facebook 开源的向量相似度搜索库，常用于 RAG 系统的向量存储。"
        ]
        
        results = []
        for i, doc in enumerate(fallback_docs[:top_k], 1):
            results.append({
                "content": doc,
                "score": 0.85,
                "source": "fallback_knowledge_base"
            })
        
        print(f"[RAG] 使用备用检索，返回 {len(results)} 条结果")
        
        return results
    
    def format_results(self, results: List[Dict]) -> str:
        """格式化检索结果"""
        formatted_parts = []
        
        for i, result in enumerate(results, 1):
            content = result['content']
            score = result.get('score', 0)
            source = result.get('source', 'unknown')
            
            formatted_parts.append(
                f"[文档{i}] 来源: {source}\n"
                f"内容: {content[:300]}{'...' if len(content) > 300 else ''}\n"
                f"相关性评分: {score:.4f}"
            )
        
        return "\n\n".join(formatted_parts)


def create_rag_retriever(config: dict = None) -> RAGRetriever:
    """创建 RAG 检索器实例"""
    return RAGRetriever(config)


async def test_rag_system():
    """测试 RAG 系统"""
    retriever = create_rag_retriever()
    
    test_queries = [
        "什么是 LangGraph？",
        "如何使用 StateGraph？",
        "DeepSeek 模型有什么特点？"
    ]
    
    print("\n=== RAG 系统测试 ===\n")
    
    for query in test_queries:
        print(f"查询: {query}")
        results = await retriever.retrieve(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n结果{i} (相关性: {result['score']:.4f}):")
            print(result['content'][:200])
        
        print("-" * 50)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_rag_system())
