import requests
import config
import random


def get_sentence():
    fallback_sentences = [
        "生活不止眼前的苟且，还有永远写不完的代码。",
        "别沮丧，你只是运气差，并不是不努力。",
        "今天又是元气满满（骗自己的）的一天！",
        "你不是胖，只是喜欢被地球引力紧紧拥抱。",
        "你以为努力就有回报？不，得别人不努力。",
        "代码不规范，亲人两行泪。",
        "没有什么是一行 `print()` 解决不了的，如果有，那就两行。",
        "卷是解决不了问题的，但不卷你可能连机会都没了。",
        "你已经很优秀了，只是还没人发现（包括你自己）。",
        "上帝为你关上一扇门，还会顺手关掉灯，拔掉网线。"
    ]

    try:
        url = config.FUNNY_SENTENCE_URRL
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # 如果data结构异常，则fallback
        if "data" in data and isinstance(data["data"], str):
            return data["data"]
        else:
            raise ValueError("返回数据结构异常")

    except Exception as e:
        # 日志可选：print(f"获取每日一句失败：{e}")
        return random.choice(fallback_sentences)
