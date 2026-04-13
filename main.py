import asyncio
import sys
from src.agent.graph import agent
from src.agent.config import config


def get_default_config():
    """获取默认配置（从 config.yaml 读取）"""
    return {
        "configurable": config.get_context_config()
    }


async def run_agent(user_input: str, config_override: dict = None):
    """运行 Agent 工作流"""
    final_config = config_override or get_default_config()
    
    model_config = config.model_config
    model_name = final_config["configurable"].get("model_name", "deepseek-chat")
    
    print(f"\n{'='*60}")
    print(f"🚀 启动 LangGraph Agent 工作流")
    print(f"{'='*60}")
    print(f"🤖 模型: {model_name}")
    print(f"💬 用户输入: {user_input}")
    print('='*60)
    
    input_data = {"user_input": user_input}
    
    try:
        result = await agent.ainvoke(input_data, config=final_config)
        
        print(f"\n✅ 执行完成!")
        print(f"\n📝 最终回答:\n{result['final_response']}")
        print(f"\n📊 执行统计:")
        print(f"   - 路由决策: {result['route_decision']}")
        if result.get('tool_results'):
            print(f"   - 🔧 使用工具: {len(result['tool_results'])} 个")
            for tool_result in result['tool_results']:
                print(f"      • {tool_result['tool_name']}: {str(tool_result['result'])[:50]}...")
        if result.get('rag_results'):
            print(f"   - 📚 RAG 检索: {len(result['rag_results'])} 条结果")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 执行失败!")
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def interactive_mode():
    """交互模式"""
    model_config = config.model_config
    
    print("\n" + "="*60)
    print("🤖 LangGraph Agent 交互模式 (DeepSeek + RAG)")
    print("="*60)
    print(f"📌 模型: {config._config['model']['name']}")
    print(f"📌 RAG: {'✅ 已启用' if config._config['rag']['enabled'] else '❌ 已禁用'}")
    print(f"📌 工具: {'✅ 已启用' if config._config['tools']['enabled'] else '❌ 已禁用'}")
    print(f"📌 记忆: {'✅ 已启用' if config._config['memory']['enabled'] else '❌ 已禁用'}")
    print("="*60)
    print("💡 输入 'quit' 或 'exit' 退出\n")
    
    while True:
        try:
            user_input = input("你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见!")
                break
            
            if not user_input:
                continue
            
            await run_agent(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            break
        except Exception as e:
            print(f"\n⚠️ 错误: {str(e)}")


async def demo_mode():
    """演示模式 - 展示各种场景"""
    print("\n" + "="*60)
    print("🎯 LangGraph Agent 功能演示")
    print("="*60)
    
    test_cases = [
        ("你好，请介绍一下你自己", "LLM直接回答"),
        ("帮我计算 123 * 456", "工具调用"),
        ("什么是 LangGraph？", "RAG检索"),
        ("今天北京天气怎么样", "工具调用"),
        ("如何使用 StateGraph 构建工作流？", "RAG检索"),
    ]
    
    for i, (user_input, scenario) in enumerate(test_cases, 1):
        print(f"\n{'─'*60}")
        print(f"📝 场景{i}: {scenario}")
        print(f"{'─'*60}")
        
        await run_agent(user_input)
        
        if i < len(test_cases):
            input("\n按 Enter 继续...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            asyncio.run(demo_mode())
        else:
            user_input = " ".join(sys.argv[1:])
            asyncio.run(run_agent(user_input))
    else:
        asyncio.run(interactive_mode())
