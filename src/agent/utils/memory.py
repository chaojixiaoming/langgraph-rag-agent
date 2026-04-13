from typing import Dict, Any, List
import json
from datetime import datetime


class MemoryManager:
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or "memory.json"
        self.memory_store: Dict[str, Any] = {}
    
    def save_memory(self, session_id: str, data: Dict[str, Any]) -> bool:
        """保存记忆数据"""
        try:
            timestamp = datetime.now().isoformat()
            memory_entry = {
                "session_id": session_id,
                "timestamp": timestamp,
                "data": data,
                "type": "conversation_memory"
            }
            
            if session_id not in self.memory_store:
                self.memory_store[session_id] = []
            self.memory_store[session_id].append(memory_entry)
            
            return True
        except Exception as e:
            print(f"保存记忆失败: {e}")
            return False
    
    def load_memory(self, session_id: str) -> List[Dict[str, Any]]:
        """加载记忆数据"""
        return self.memory_store.get(session_id, [])
    
    def format_memory_for_context(self, session_id: str) -> str:
        """格式化记忆用于上下文"""
        memories = self.load_memory(session_id)
        if not memories:
            return ""
        
        formatted = ["历史对话记录:"]
        for mem in memories[-5:]:
            formatted.append(f"- [{mem['timestamp']}] {mem['data'].get('user_input', '')} -> {mem['data'].get('response', '')}")
        
        return "\n".join(formatted)


def create_memory_manager(storage_path: str = None) -> MemoryManager:
    """创建记忆管理器实例"""
    return MemoryManager(storage_path)
