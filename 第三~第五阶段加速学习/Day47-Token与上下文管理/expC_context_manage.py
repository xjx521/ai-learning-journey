# from openai import OpenAI
# from dotenv import load_dotenv
# import os
import re

# load_dotenv()


def count_messages_tokens(messages):
    text = "".join(
        m["content"] for m in messages
    )  # messages是列表列表里面嵌套了字典 需要提取的是里面的content
    count_chinese = len(re.findall(r"[一-鿿]", text))
    count_english = len(re.findall(r"[a-zA-Z]+", text))
    count_symbol = len(
        re.findall(r"[^一-鿿a-zA-Z\s]", text)
    )  # 数"除中英文和空白以外"的字符
    # 正常分词器会把英文和空格估算成一个token如:"hello world" 分成"hello" " world"

    total_token = count_chinese * 1.5 + count_english * 1.3 + count_symbol * 1
    return round(total_token, 1)


def manage_history(messages, limit):  # ：limit 是 token 数，不是消息条数
    while count_messages_tokens(messages) > limit:
        if (
            len(messages) <= 5
        ):  # 1 条 system + 2 对（user+assistant）= 5 条。删到只剩 5 条就必须停，哪怕token 还超
            break

        del messages[1:3]
        # messages.pop(1)
        # messages.pop(1)  # 不需要pop(1)再pop(2)这样下标会前移原来的下标为2就跑到1去了

    return messages


# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com/v1",
# )


# def send_message(message):
#     response = client.chat.completions.create(
#         model="deepseek-v4-flash",
#         messages=message,
#     )
#     return response.choices[0].message


message = [
    {
        "role": "system",
        "content": "你是一个耐心的客服助手，负责解答用户的订单和物流问题。",
    }
]
# 单价
PRICE_INPUT = 1.0 / 1000000  # 输入单价 元/token（缓存未命中，常规场景）
PRICE_OUTPUT = 2.0 / 1000000  # 输出单价 元/token
limit = 800
for i in range(20):
    message.append(
        {"role": "user", "content": f"第{i+1}轮：我想查一下订单什么时候发货"}
    )
    # —— TODO：此刻量【输入】—— 现在列表里没有这轮的 assistant，量到的就是输入
    input_tokens = count_messages_tokens(message)
    # 模拟ai回答
    message.append(
        {
            "role": "assistant",
            "content": f"第{i+1}轮：您的订单预计明天发货，物流单号是...",
        }
    )
    output_tokens = count_messages_tokens([message[-1]])  ##   只量最后这一条！
    total = count_messages_tokens(message)  # 这轮累积了多少 token
    message = manage_history(
        message, limit
    )  # 超限就截断（注意它就地改，再赋值回去即可）
    if i == 4:
        total_cost = PRICE_INPUT * input_tokens + PRICE_OUTPUT * PRICE_OUTPUT
        print(f"这是第{i+1}轮")
        print(f"本轮累计耗费：{total} tokens")
        print("超 limit 吗", total > limit)
        print(f"预估累计成本:{total_cost:.4f}")
    if i == 9:
        total_cost = PRICE_INPUT * input_tokens + PRICE_OUTPUT * PRICE_OUTPUT
        print(f"这是第{i+1}轮")
        print(f"本轮累计耗费：{total} tokens")
        print("超 limit 吗", total > limit)
        print(f"预估累计成本:{total_cost:.4f}")
    if i == 19:
        total_cost = PRICE_INPUT * input_tokens + PRICE_OUTPUT * PRICE_OUTPUT
        print(f"这是第{i+1}轮")
        print(f"本轮累计耗费：{total} tokens")
        print("超 limit 吗", total > limit)
        print(f"预估累计成本:{total_cost:.4f}")

new_context = (len(message) - 1) // 2
print(f"manage_history 后剩{new_context}轮")
