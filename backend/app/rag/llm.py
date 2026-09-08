"""DeepSeek 调用封装: OpenAI 兼容协议, 直接 HTTP POST"""
import httpx

from app import config

MODEL = "deepseek-v4-flash"  # 对话模型; deepseek-reasoner 是推理模型(贵、慢)


def chat(messages, temperature=0.3, max_tokens=1024):
    """messages: [{"role": "system"/"user", "content": "..."}] → 返回回答文本"""
    if not config.DEEPSEEK_API_KEY:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY, 请在 backend/.env 中填写")

    resp = httpx.post(
        f"{config.DEEPSEEK_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {config.DEEPSEEK_API_KEY}"},
        json={
            "model": MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "thinking": {"type": "enabled"},
            "reasoning_effort": "low",
            "stream": False,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
