import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """统一配置管理器"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls, config_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config_path: str = None):
        if not self._config:
            self.load_config(config_path)
    
    def load_config(self, config_path: str = None):
        """加载配置文件"""
        if config_path is None:
            # 从 src/agent/ 向上3级到达项目根目录
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config.yaml"
        
        if not Path(config_path).exists():
            raise FileNotFoundError(
                f"配置文件不存在: {config_path}\n"
                f"当前工作目录: {Path.cwd()}\n"
                f"请确保 config.yaml 位于项目根目录"
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        
        from dotenv import load_dotenv
        # 加载项目根目录的 .env 文件
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print(f"[Config] 已加载环境变量文件: {env_file}")
        else:
            load_dotenv()
            print(f"[Config] 使用默认 .env 文件")
    
    @property
    def model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        import os
        return {
            "model_name": self._config["model"]["name"],
            "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
            "api_base": self._config["model"]["api_base"],
            "temperature": self._config["model"]["temperature"],
            "max_tokens": self._config["model"]["max_tokens"]
        }
    
    @property
    def rag_config(self) -> Dict[str, Any]:
        """获取 RAG 配置"""
        return {
            "enabled": self._config["rag"]["enabled"],
            "chunk_size": self._config["rag"]["chunk_size"],
            "chunk_overlap": self._config["rag"]["chunk_overlap"],
            "top_k": self._config["rag"]["top_k"],
            **self._config["rag"].get("vector_db", {})
        }
    
    @property
    def tools_config(self) -> Dict[str, Any]:
        """获取工具配置"""
        return {
            "enabled": self._config["tools"]["enabled"],
            "available_tools": self._config["tools"]["available_tools"]
        }
    
    @property
    def memory_config(self) -> Dict[str, Any]:
        """获取记忆配置"""
        return {
            "enabled": self._config["memory"]["enabled"],
            "storage_path": self._config["memory"]["storage_path"],
            "max_history": self._config["memory"]["max_history"]
        }
    
    @property
    def agent_config(self) -> Dict[str, Any]:
        """获取 Agent 配置"""
        return self._config.get("agent", {})
    
    def get_context_config(self) -> Dict[str, Any]:
        """生成 LangGraph Context 配置"""
        return {
            "model_name": self._config["model"]["name"],
            "temperature": self._config["model"]["temperature"],
            "max_tokens": self._config["model"]["max_tokens"],
            "use_rag": self._config["rag"]["enabled"],
            "use_tools": self._config["tools"]["enabled"],
            "rag_config": self.rag_config,
            "memory_enabled": self._config["memory"]["enabled"]
        }


def load_config(config_path: str = None) -> Config:
    """加载配置（单例模式）"""
    return Config(config_path)


config = Config()
