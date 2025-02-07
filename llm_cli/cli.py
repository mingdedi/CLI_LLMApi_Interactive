import cmd
from .config_loader import load_config
from typing import Dict, Any
from .chat_session import OpenAIChatSession
from .config_loader import get_model_names,get_model_config
import argparse

class CommandHandler:
    """命令处理核心类"""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_session = None

    def handle_model_list(self, *args):
        """处理 model_list 命令"""
        models = get_model_names(self.config)
        print("\nAvailable models:")
        print("-" * 30)
        for model in models:
            print(f"  • {model}")
        print()

    def handle_interactive(self, model_name: str,stream=False,json=False):
        """处理 interactive 命令"""
        model_config = get_model_config(self.config, model_name)
        if not model_config:
            print(f"\nError: Model '{model_name}' not found in config\n")
            return

        #根据提供商创建会话
        self.active_session = OpenAIChatSession(model_config)

        print(f"\nEntering {model_name} interactive mode (type 'quit' to exit)")
        while True:
            try:
                user_input = input("> ")
                if user_input.strip().lower() == "quit":
                    break
                self.active_session.generate_response(user_input,stream=stream,json=json)
            except KeyboardInterrupt:
                print("\nExiting interactive mode...\n")
                break


class LLMCLI(cmd.Cmd):
    """命令行交互主程序"""
    prompt = "(llm-cli) > "
    
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.handler = CommandHandler(self.config)

    def do_model_list(self, arg):
        """列出所有可用模型"""
        self.handler.handle_model_list()

    def do_interactive(self, arg):
        """启动交互模式：interactive <model-name> [--stream] [--json]"""
        parser = argparse.ArgumentParser(description="Interactive mode with optional streaming.")
        parser.add_argument("model_name", type=str, help="The name of the model to use.")
        parser.add_argument("--stream", action="store_true", help="Enable streaming mode.")
        parser.add_argument("--json", action="store_true", help="Enable json mode.")

        try:
            args = parser.parse_args(arg.split())
        except SystemExit:
            print("Error: Paramenter")
            return  # 防止 argparse 在解析失败时退出程序
        
        self.handler.handle_interactive(args.model_name, stream=args.stream,json=args.json)

    def do_quit(self, arg):
        """退出程序"""
        print("Exiting...")
        return True