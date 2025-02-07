import json
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """加载配置文件"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file {config_path} not found")
    with open(path, "r") as f:
        return json.load(f)

def get_model_names(config: Dict[str, Any]) -> list:
    """获取可用模型列表"""
    return list(config.get("models", {}).keys())

def get_model_config(config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """获取指定模型配置"""
    return config["models"].get(model_name)

if __name__ == "__main__":
    config_json=load_config("config.json")#返回的是一个字典型变量
    model_names=get_model_names(config_json)
    model_config=get_model_config(config_json,model_names[0])
    print(model_config)