# CLI_LLMApi_Interactive
一个典型的config.json格式
```json
{
    "models": {
      "DeepSeek/deepseek-r1": {
        "provider": "DeepSeek",
        "api_key": "",
        "model_id": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com", 
        "temperature": 0.7,
        "max_tokens": 4096
      },
      "DeepSeek/deepseek-v3": {
        "provider": "DeepSeek",
        "api_key": "",
        "model_id": "deepseek-chat",
        "base_url": "https://api.deepseek.com", 
        "temperature": 0.7,
        "max_tokens": 4096
      }
    }
}
  
```