from typing import List, Dict, Any, Optional
import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.agent.config import config


class VectorDBManager:
    """向量数据库管理器"""
    
    def __init__(self, config_override: dict = None):
        self.config = config_override or config.rag_config
        self.vector_store: Optional[FAISS] = None
        self.embeddings = None
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """初始化 Embedding 模型"""
        model_name = self.config.get("embedding_model", "BAAI/bge-small-zh-v1.5")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def load_documents(self, file_path: str) -> List:
        """加载文档"""
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        
        print(f"[VectorDB] 加载文档: {file_path}")
        print(f"[VectorDB] 文档数量: {len(documents)}")
        
        return documents
    
    def split_documents(self, documents: List) -> List:
        """分割文档"""
        chunk_size = self.config.get("chunk_size", 500)
        chunk_overlap = self.config.get("chunk_overlap", 50)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ";", "；", "，", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        
        print(f"[VectorDB] 文档分割完成")
        print(f"[VectorDB] 分块数量: {len(chunks)}")
        
        return chunks
    
    def create_vector_store(self, chunks: List, persist_dir: str = None):
        """创建向量数据库"""
        persist_dir = persist_dir or self.config.get("persist_directory", "./vector_db")
        
        if os.path.exists(persist_dir):
            self.vector_store = FAISS.load_local(
                persist_dir,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"[VectorDB] 从本地加载向量库: {persist_dir}")
        else:
            self.vector_store = FAISS.from_documents(
                chunks,
                self.embeddings
            )
            
            os.makedirs(persist_dir, exist_ok=True)
            self.vector_store.save_local(persist_dir)
            print(f"[VectorDB] 创建并保存向量库到: {persist_dir}")
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """检索相关文档"""
        if not self.vector_store:
            raise ValueError("向量数据库未初始化，请先调用 create_vector_store")
        
        top_k = top_k or self.config.get("top_k", 3)
        
        results = self.vector_store.similarity_search_with_score(query, k=top_k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(1 - score),
                "source": doc.metadata.get("source", "unknown")
            })
        
        print(f"[VectorDB] 检索完成，返回 {len(formatted_results)} 条结果")
        
        return formatted_results
    
    def format_results(self, results: List[Dict]) -> str:
        """格式化检索结果"""
        formatted_parts = []
        
        for i, result in enumerate(results, 1):
            content = result['content']
            score = result['score']
            source = result.get('source', 'unknown')
            
            formatted_parts.append(
                f"[文档{i}] 来源: {source}\n"
                f"内容: {content}\n"
                f"相关性评分: {score:.4f}"
            )
        
        return "\n\n".join(formatted_parts)


def create_vector_db_manager(config_override: dict = None) -> VectorDBManager:
    """创建向量数据库管理器实例"""
    return VectorDBManager(config_override)


def initialize_knowledge_base(knowledge_file: str = None, config_override: dict = None) -> VectorDBManager:
    """初始化知识库（一站式函数）"""
    manager = create_vector_db_manager(config_override)
    
    if knowledge_file is None:
        knowledge_file = Path(__file__).parent.parent.parent / "data" / "knowledge_base.txt"
    
    documents = manager.load_documents(str(knowledge_file))
    chunks = manager.split_documents(documents)
    manager.create_vector_store(chunks)
    
    return manager
