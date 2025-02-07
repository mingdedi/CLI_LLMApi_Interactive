from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BaseChatSession(ABC):
    """对话会话基类（抽象层）"""
    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config
        self.history: List[Dict[str, str]] = []

    @abstractmethod
    def generate_response(self, user_input: str) -> str:
        """生成模型响应（需子类实现）"""
        pass

class OpenAIChatSession(BaseChatSession):
    """OpenAI 会话实现"""
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        from openai import OpenAI
        self.client = OpenAI(#将根据传入的配置进行配置初始化
            api_key=self.model_config["api_key"],
            base_url=self.model_config["base_url"]
        )

    def generate_response(self, user_input: str,stream=False,json=False) -> str:
        self.history.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model=self.model_config["model_id"],
            messages=self.history,
            temperature=self.model_config.get("temperature", 0.7),
            max_tokens=self.model_config.get("max_tokens", 1024),
            stream=stream
        )
        if(json==True):
            print(f"\n{response}\n")
            assistant_reply = response.choices[0].message.content
        elif(stream==True):
            assistant_reply=[]
            print(f"\nAssistant: ",end="", flush=True)
            for chunk in response:
                token_response = chunk.choices[0].delta.content or ""
                print(token_response, end="", flush=True)
                assistant_reply.append(token_response)
            print("\n", flush=True)
            assistant_reply="".join(assistant_reply)  
        else:
            assistant_reply = response.choices[0].message.content
            print(f"\nAssistant: {assistant_reply}\n")
        self.history.append({"role": "assistant", "content": assistant_reply})
        return self.history[-1]