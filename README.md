# 🤖 LangGraph Agent - DeepSeek + RAG + Tools

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://langchain-ai.github.io/langgraph/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-Chat-orange.svg)](https://platform.deepseek.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于 **LangGraph** 最新版本构建的智能 Agent 系统，集成 **DeepSeek** 大模型、**RAG 知识库检索**、**工具调用** 和 **记忆管理**。

## ✨ 核心特性

- 🧠 **智能路由**: 自动判断是否需要调用工具或使用 RAG 检索
- 🔧 **工具集成**: 内置搜索、计算、天气等工具，支持扩展
- 📚 **RAG 检索**: 基于 FAISS 向量数据库的知识库问答
- 💾 **记忆系统**: 对话历史持久化存储
- ⚙️ **配置驱动**: YAML 配置文件，灵活调整参数
- 🚀 **DeepSeek**: 使用高性能中文大模型
- 🎯 **工程化设计**: 符合 LangGraph 官方最佳实践

## 🏗️ 项目架构

### 工作流程图

```
用户输入 → [Router 路由判断]
    ├─→ 不需要工具 → [LLM 直接回答] ─┐
    └─→ 需要工具/RAG → [工具执行] → [结果整理] ─┤
                                                ↓
                                      [生成最终回答] → [保存记忆]
```

### 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| **框架** | LangGraph | ≥0.2.0 |
| **大模型** | DeepSeek Chat | latest |
| **向量数据库** | FAISS (CPU) | ≥1.7.4 |
| **Embedding** | BAAI/bge-small-zh-v1.5 | ≥2.2.0 |
| **配置管理** | PyYAML | ≥6.0 |
| **包管理** | pyproject.toml | PEP 517 |

## 📁 项目结构

```
project/
├── config.yaml                    # 统一配置文件（模型、RAG、工具等）
├── pyproject.toml                 # Python 项目配置和依赖
├── langgraph.json                 # LangGraph 部署配置
├── .env                           # 环境变量（API Key）
├── main.py                        # 主入口文件
│
├── data/                          # 数据目录
│   └── knowledge_base.txt         # LangGraph 知识库文档
│
├── src/agent/                     # Agent 核心代码
│   ├── config.py                  # 配置管理器（单例模式）
│   ├── state.py                   # 图状态定义
│   ├── context.py                 # 运行时上下文
│   ├── graph.py                   # 工作流图构建
│   │
│   ├── nodes/                     # 节点实现
│   │   ├── router.py              # 路由判断节点
│   │   ├── llm_direct.py          # LLM 直接回答节点
│   │   ├── tool_executor.py       # 工具执行/RAG 检索节点
│   │   ├── result_formatter.py    # 结果整理节点
│   │   ├── response_generator.py  # 最终回答生成节点
│   │   └── memory_saver.py        # 记忆保存节点
│   │
│   └── utils/                     # 工具模块
│       ├── tools.py               # 工具定义（搜索、计算、天气）
│       ├── rag.py                 # RAG 检索器（对接向量库）
│       ├── vector_db.py           # FAISS 向量数据库管理
│       └── memory.py              # 记忆管理系统
│
├── scripts/                       # 辅助脚本
│   ├── init_vector_db.py          # 初始化向量数据库
│   ├── verify_imports.py          # 验证模块导入
│   └── verify_paths.py            # 验证路径配置
│
└── tests/                         # 测试套件
    ├── test_nodes.py              # 节点单元测试
    ├── test_graph.py              # 图构建测试
    └── test_quick_run.py          # 快速功能验证
```

## 🚀 快速开始

### 前提条件

- Python 3.10 或更高版本
- DeepSeek API Key（从 [DeepSeek 平台](https://platform.deepseek.com/) 获取）

### 安装步骤

#### 1️⃣ 克隆项目并进入目录

```bash
cd d:\uu\cod\newproject
```

#### 2️⃣ 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3️⃣ 安装依赖

```bash
pip install -e .
```

或安装开发依赖：

```bash
pip install -e ".[dev]"
```

**主要依赖包括：**
- `langgraph` - LangGraph 框架
- `langchain-openai` - OpenAI 兼容接口（用于 DeepSeek）
- `langchain-community` - 社区组件
- `faiss-cpu` - FAISS 向量数据库
- `sentence-transformers` - Embedding 模型
- `pyyaml` - YAML 配置解析

#### 4️⃣ 配置环境变量

编辑 `.env` 文件，填入你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=sk-your_actual_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

> ⚠️ **注意**: 不要将包含真实 API Key 的 `.env` 文件提交到 Git！

#### 5️⃣ 初始化向量数据库

```bash
python scripts/init_vector_db.py
```

这将：
1. 加载 `data/knowledge_base.txt` 知识库文件
2. 使用中文 Embedding 模型向量化文本
3. 创建并保存 FAISS 向量索引到 `./vector_db/` 目录

**预期输出：**
```
🚀 初始化 LangGraph 知识库向量数据库
============================================================

📋 配置信息:
   - Embedding 模型: BAAI/bge-small-zh-v1.5
   - 分块大小: 500
   - 重叠大小: 50
   - 存储路径: ./vector_db

📚 知识库文件: data/knowledge_base.txt
   文件大小: xx.xx KB

✅ 向量数据库初始化成功!
```

#### 6️⃣ 启动 Agent

**交互模式（推荐）：**
```bash
python main.py
```

**命令行模式：**
```bash
python main.py "什么是 LangGraph？"
```

**演示模式（展示所有功能）：**
```bash
python main.py --demo
```

## 🎮 使用示例

### 场景 1：LLM 直接回答

```
你: 你好，请介绍一下你自己

🤖 Agent: 我是基于 LangGraph 和 DeepSeek 构建的智能助手...
```

**路由决策**: `direct_llm`（不需要工具）

---

### 场景 2：工具调用

```
你: 帮我计算 123 * 456

🔧 [Tool Executor] 执行工具调用...
[Tool Executor] 工具 calculator 执行完成

🤖 Agent: 计算结果为: 56088
```

**路由决策**: `need_tools`（触发计算器工具）

---

### 场景 3：RAG 知识库检索

```
你: 什么是 StateGraph？

📚 [Tool Executor] 执行 RAG 检索...
[RAG] 从向量库检索到 3 条结果

🤖 Agent: StateGraph 是 LangGraph 的核心组件，用于构建状态图...
```

**路由决策**: `need_rag`（触发知识库检索）

---

### 场景 4：天气查询

```
你: 今天北京天气怎么样？

🤖 Agent: 北京今天的天气是晴天，温度约 25°C
```

**路由决策**: `need_tools`（触发天气查询工具）

## ⚙️ 配置说明

### config.yaml 主要参数

```yaml
model:
  name: "deepseek-chat"           # 模型名称
  provider: "deepseek"
  api_base: "https://api.deepseek.com/v1"
  temperature: 0.7                # 生成温度（0-2）
  max_tokens: 2000                # 最大生成长度

rag:
  enabled: true                   # 是否启用 RAG
  chunk_size: 500                 # 文档分块大小
  chunk_overlap: 50               # 分块重叠大小
  top_k: 3                        # 检索返回数量
  vector_db:
    type: "faiss"
    persist_directory: "./vector_db"  # 向量库存储路径
    embedding_model: "BAAI/bge-small-zh-v1.5"

tools:
  enabled: true                   # 是否启用工具
  available_tools:                # 可用工具列表
    - search_web
    - calculator
    - get_weather

memory:
  enabled: true                   # 是否启用记忆
  storage_path: "./memory.json"
  max_history: 10                 # 最大历史记录数

agent:
  route_keywords_tools:           # 触发工具调用的关键词
    - "搜索"
    - "计算"
    - "天气"
    - "查询"
  route_keywords_rag:             # 触发 RAG 检索的关键词
    - "什么是"
    - "如何"
    - "介绍"
    - "文档"
```

### 动态修改配置

可以在代码中覆盖默认配置：

```python
from src.agent.config import config

# 获取当前配置
print(config.model_config)

# 运行时修改（需要重新加载）
custom_config = {
    "configurable": {
        "model_name": "deepseek-chat",
        "temperature": 0.9,  # 更有创造性
        "use_rag": True,
        "use_tools": True
    }
}

result = await agent.ainvoke(
    {"user_input": "你的问题"},
    config=custom_config
)
```

## 🧪 测试

### 运行所有测试

```bash
pytest tests/ -v
```

### 单独运行测试

```bash
# 节点单元测试
pytest tests/test_nodes.py -v

# 图构建测试
pytest tests/test_graph.py -v

# 快速功能验证（无需 API Key）
python tests/test_quick_run.py
```

### 验证工具

```bash
# 验证模块导入
python scripts/verify_imports.py

# 验证路径配置
python scripts/verify_paths.py
```

## 🛠️ 开发指南

### 添加新工具

1. 在 `src/agent/utils/tools.py` 中定义新工具：

```python
@tool
def my_new_tool(param: str) -> str:
    """工具描述"""
    return f"处理结果: {param}"
```

2. 将工具添加到 `TOOLS` 列表：

```python
TOOLS = [search_web, calculator, get_weather, my_new_tool]
```

3. 在 `config.yaml` 中注册工具名称：

```yaml
tools:
  available_tools:
    - my_new_tool
```

### 扩展知识库

1. 编辑 `data/knowledge_base.txt`，添加新的文档内容
2. 重新初始化向量数据库：

```bash
python scripts/init_vector_db.py
```

### 自定义 Embedding 模型

在 `config.yaml` 中修改：

```yaml
rag:
  vector_db:
    embedding_model: "your-custom-model-name"
```

支持的模型：
- 中文: `BAAI/bge-small-zh-v1.5`, `BAAI/bge-base-zh-v1.5`
- 英文: `all-MiniLM-L6-v2`, `all-mpnet-base-v2`
- 多语言: `multilingual-e5-small`, `paraphrase-multilingual-MiniLM-L12-v2`

## 📊 性能优化建议

### 1. 向量数据库优化

```bash
# 使用 GPU 加速（如果可用）
pip install faiss-gpu

# 在 config.yaml 中启用
rag:
  vector_db:
    type: "faiss-gpu"
```

### 2. Embedding 模型选择

| 模型 | 大小 | 速度 | 质量 | 适用场景 |
|------|------|------|------|----------|
| bge-small-zh | ~100MB | ⚡⚡⚡ | ✅ | 生产环境 |
| bge-base-zh | ~400MB | ⚡⚡ | ✅✅ | 高质量需求 |
| bge-large-zh | ~1.3GB | ⚡ | ✅✅✅ | 精确匹配 |

### 3. RAG 参数调优

- **chunk_size**: 增大可保留更多上下文，但降低检索精度
- **top_k**: 增大提供更多参考信息，但增加 token 消耗
- **chunk_overlap**: 推荐设置为 chunk_size 的 10%

## ❓ 常见问题

### Q1: ImportError: cannot import name 'Runtime'

**原因**: LangGraph 版本更新导致 API 变化。

**解决**: 已修复，确保代码中使用：
```python
from langgraph.runtime import Runtime  # ✅ 正确
# 不是 from langgraph.types import Runtime  # ❌ 错误
```

### Q2: FileNotFoundError: config.yaml

**原因**: 配置文件路径不正确。

**解决**: 
1. 确保 `config.yaml` 位于项目根目录
2. 运行 `python scripts/verify_paths.py` 验证路径

### Q3: 向量数据库初始化失败

**可能原因**:
- 未安装 `sentence-transformers`: `pip install sentence-transformers`
- 网络问题无法下载模型
- 磁盘空间不足

**解决方案**:
```bash
# 手动下载模型（离线环境）
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
model.save('./local_model')

# 然后在 config.yaml 中指定本地路径
embedding_model: "./local_model"
```

### Q4: DeepSeek API 调用失败

**检查项**:
1. API Key 是否正确（无多余空格）
2. 账户余额是否充足
3. 网络连接是否正常（国内可能需要代理）

**调试方法**:
```python
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)
response = llm.invoke("Hello")
print(response.content)
```

### Q5: 如何切换到其他模型？

支持任何 OpenAI 兼容的 API：

```yaml
# config.yaml
model:
  name: "gpt-4o"              # 或 "claude-3-opus", "qwen-turbo" 等
  api_base: "https://api.openai.com/v1"
```

然后在 `.env` 中设置对应的 API Key。

## 📈 项目路线图

- [x] 基础架构搭建
- [x] DeepSeek 模型集成
- [x] RAG + FAISS 向量数据库
- [x] 工具调用系统
- [x] 记忆管理
- [ ] 多轮对话上下文管理
- [ ] 流式输出支持
- [ ] LangGraph Studio 可视化
- [ ] Docker 容器化部署
- [ ] REST API 接口
- [ ] Web UI 前端

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [LangChain/LangGraph](https://github.com/langchain-ai/langgraph) - 强大的 AI 应用框架
- [DeepSeek](https://platform.deepseek.com/) - 高性能大语言模型
- [FAISS](https://github.com/facebookresearch/faiss) - 高效向量搜索库
- [Hugging Face](https://huggingface.co/) - 开源模型和工具生态

---

## 📞 支持

如有问题，请：
1. 查看 [常见问题](#❓-常见问题) 章节
2. 运行验证脚本排查问题
3. 提交 Issue 或 Discussion

**Happy Coding! 🚀**
