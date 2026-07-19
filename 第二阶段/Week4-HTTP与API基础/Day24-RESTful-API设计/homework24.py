"""
Day 24 练习题：RESTful API 设计 + JSON
====================================

💡 提示：今天主要是"设计题"，不用写太多代码，重点训练 API 设计思维。
"""

import json


# ============================================================
# 【练习 1】RESTful API 设计（核心练习）
# ============================================================
"""
场景：你要为一个"在线书店"设计 RESTful API。
请根据以下需求，设计合适的 URL + HTTP 方法 + 状态码。

格式示例：
  需求：查看书店所有书籍
  设计：GET /books → 200

请按同样的格式完成以下设计：

1. 查看所有书籍列表
   你的设计：____________________________________

2. 查看某一本书的详细信息（通过 ID）
   你的设计：____________________________________

3. 添加一本新书到书店
   你的设计：____________________________________

4. 更新某本书的全部信息（标题、价格、描述等全改）
   你的设计：____________________________________

5. 只修改某本书的价格
   你的设计：____________________________________

6. 删除一本书
   你的设计：____________________________________

7. 搜索书籍（按关键词 + 价格范围 + 分页）
   你的设计：____________________________________

8. 查看某本书的所有评论
   你的设计：____________________________________

9. 给某本书添加一条评论
   你的设计：____________________________________

10. 删除某条评论
    你的设计：____________________________________
"""

# ==================== 参考答案 ====================
def check_exercise_1():
    print("=" * 50)
    print("【练习 1 参考答案】在线书店 API 设计")
    print("=" * 50)
    answers = [
        ("1. 查看所有书籍",     "GET    /books                                    → 200"),
        ("2. 查看一本书详情",   "GET    /books/{book_id}                        → 200"),
        ("3. 添加新书",        "POST   /books                                   → 201"),
        ("4. 更新书的全部信息", "PUT    /books/{book_id}                        → 200"),
        ("5. 只修改价格",      "PATCH  /books/{book_id}                        → 200"),
        ("6. 删除书",          "DELETE /books/{book_id}                        → 204"),
        ("7. 搜索书籍",        "GET    /books?keyword=python&min_price=20&max_price=100&page=1&size=20 → 200"),
        ("8. 查看书的评论",    "GET    /books/{book_id}/reviews                → 200"),
        ("9. 添加评论",        "POST   /books/{book_id}/reviews                → 201"),
        ("10. 删除评论",       "DELETE /books/{book_id}/reviews/{review_id}    → 204"),
    ]
    for desc, answer in answers:
        print(f"  {desc}")
        print(f"    {answer}\n")


# ============================================================
# 【练习 2】找茬：修正不合理的 API 设计
# ============================================================
"""
以下是一个"社交媒体"项目的 API 设计，有多处不符合 RESTful 规范。
请找出问题并修正。

原始设计：
  1. POST /api/getAllPosts         → 获取所有帖子
  2. GET  /api/addPost             → 添加新帖子（帖子数据放在 URL 参数里）
  3. POST /api/deletePost/123      → 删除 ID 为 123 的帖子
  4. GET  /api/user/123/posts      → 获取用户 123 的帖子
  5. POST /api/updatePost/123      → 更新帖子 123 的内容
  6. GET  /api/search?word=python  → 搜索帖子（keyword 参数名叫 word）

问题清单：
  第 1 条：____________________________________
  第 2 条：____________________________________
  第 3 条：____________________________________
  第 4 条：____________________________________
  第 5 条：____________________________________
  第 6 条：____________________________________
"""

# ==================== 参考答案 ====================
def check_exercise_2():
    print("=" * 50)
    print("【练习 2 参考答案】找茬修正")
    print("=" * 50)
    corrections = [
        ("1. POST /api/getAllPosts",
         "❌ URL 里有动词 + 方法用错\n   ✅ GET /api/posts"),

        ("2. GET /api/addPost",
         "❌ URL 有动词 + GET 不应创建资源 + 数据不该放 URL\n   ✅ POST /api/posts （数据放在请求体中）"),

        ("3. POST /api/deletePost/123",
         "❌ URL 有动词 + 方法用错\n   ✅ DELETE /api/posts/123"),

        ("4. GET /api/user/123/posts",
         "❌ 名词没用复数\n   ✅ GET /api/users/123/posts"),

        ("5. POST /api/updatePost/123",
         "❌ URL 有动词 + 方法应用 PUT 或 PATCH\n   ✅ PUT /api/posts/123 （全量更新）或 PATCH /api/posts/123 （部分更新）"),

        ("6. GET /api/search?word=python",
         "⚠️ 可以用，但更好的设计是直接对资源搜索\n   ✅ GET /api/posts?keyword=python"),
    ]
    for original, explanation in corrections:
        print(f"\n  原始：{original}")
        print(f"  {explanation}")
    print()


# ============================================================
# 【练习 3】JSON 数据处理
# ============================================================
def exercise_3_json_practice():
    """
    练习 Python 字典和 JSON 的互相转换
    """
    print("=" * 50)
    print("【练习 3】JSON 数据处理")
    print("=" * 50)

    # TODO 1：将以下 Python 字典转换为 JSON 字符串
    # 💡 提示：用 json.dumps()，注意 ensure_ascii=False 和 indent=2
    user_data = {
        "name": "张三",
        "age": 21,
        "is_student": True,
        "courses": ["Python", "HTTP", "FastAPI"],
        "address": {
            "city": "北京",
            "zipcode": "100000"
        },
        "girlfriend": None,
    }

    # 在这里写你的代码：
    # json_str = ???
    json_str = json.dumps(user_data, ensure_ascii=False, indent=2)

    print("\nPython 字典 → JSON 字符串：")
    print(json_str)

    # 验证
    assert '"name": "张三"' in json_str or '"name":"张三"' in json_str.replace(" ", ""), "JSON 应包含 name"
    assert "true" in json_str, "Python 的 True 应转为 JSON 的 true"
    assert "null" in json_str, "Python 的 None 应转为 JSON 的 null"
    print("✅ 转换正确！\n")

    # TODO 2：将以下 JSON 字符串解析为 Python 字典
    json_input = '''
    {
        "title": "Day 24 学习笔记",
        "tags": ["RESTful", "HTTP", "API"],
        "published": false,
        "views": 42,
        "author": null
    }
    '''

    # 在这里写你的代码：
    # parsed = ???
    parsed = json.loads(json_input)

    print("JSON 字符串 → Python 字典：")
    print(f"  标题：{parsed['title']}")
    print(f"  标签：{parsed['tags']}")
    print(f"  已发布：{parsed['published']}（Python 类型：{type(parsed['published']).__name__}）")
    print(f"  作者：{parsed['author']}（Python 类型：{type(parsed['author']).__name__}）")

    # 验证
    assert parsed["published"] is False, "JSON false 应转为 Python False"
    assert parsed["author"] is None, "JSON null 应转为 Python None"
    assert isinstance(parsed["tags"], list), "JSON 数组应转为 Python list"
    print("✅ 解析正确！\n")

    # TODO 3：读取和写入 JSON 文件
    # 💡 提示：用 json.dump() 和 json.load()（注意没有 s）
    filename = "test_data.json"

    # 写入文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已写入 {filename}")

    # 读取文件
    with open(filename, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    assert loaded_data["name"] == "张三", "读取的数据应匹配"
    print(f"✅ 读取验证通过：{loaded_data['name']}")

    # 清理测试文件
    import os
    os.remove(filename)
    print("✅ 测试文件已清理\n")


# ============================================================
# 【练习 4】设计统一响应格式
# ============================================================
"""
请设计一个统一的 API 响应格式（Python 函数），满足：

1. 成功时返回：{"code": 200, "message": "success", "data": {...}}
2. 失败时返回：{"code": 错误码, "message": "错误信息", "data": null}
3. 列表时返回：{"code": 200, "message": "success", "data": [...], "pagination": {...}}

💡 提示：写三个函数 success_response(), error_response(), list_response()
"""

# TODO：在下面实现你的函数
def success_response(data, message="success"):
    """成功响应"""
    # 在这里写你的代码
    pass

def error_response(code, message):
    """错误响应"""
    # 在这里写你的代码
    pass

def list_response(data, page, size, total):
    """列表响应（带分页）"""
    # 在这里写你的代码
    pass


# ==================== 参考答案 ====================
def success_response_answer(data, message="success"):
    return {"code": 200, "message": message, "data": data}

def error_response_answer(code, message):
    return {"code": code, "message": message, "data": None}

def list_response_answer(data, page, size, total):
    import math
    return {
        "code": 200,
        "message": "success",
        "data": data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        }
    }


def check_exercise_4():
    print("=" * 50)
    print("【练习 4 参考答案】统一响应格式")
    print("=" * 50)

    print("\n成功响应：")
    print(json.dumps(success_response_answer({"id": 1, "name": "张三"}), ensure_ascii=False, indent=2))

    print("\n错误响应：")
    print(json.dumps(error_response_answer(404, "用户不存在"), ensure_ascii=False, indent=2))

    print("\n列表响应：")
    users = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
    print(json.dumps(list_response_answer(users, page=1, size=20, total=55), ensure_ascii=False, indent=2))
    print()


# ============================================================
# 【练习 5】状态码选择挑战
# ============================================================
"""
为以下每个场景选择最合适的 HTTP 状态码：

1. 用户注册成功 → _____
2. 用户请求的资源格式不支持（如请求 XML 但只支持 JSON）→ _____
3. 用户上传的文件太大，超出限制 → _____
4. 用户短时间内发送了太多请求 → _____
5. 服务器正在维护，暂时不可用 → _____
6. 请求成功，但返回的数据是缓存中的旧数据 → _____（提示：不是 200）
7. 创建资源成功，但不需要返回内容 → _____（提示：不是 201）
8. 请求需要重定向到新的 URL → _____
"""

# ==================== 参考答案 ====================
def check_exercise_5():
    print("=" * 50)
    print("【练习 5 参考答案】状态码选择")
    print("=" * 50)
    answers = [
        ("1. 注册成功", "201 Created"),
        ("2. 格式不支持", "406 Not Acceptable 或 415 Unsupported Media Type"),
        ("3. 文件太大", "413 Payload Too Large"),
        ("4. 请求太多", "429 Too Many Requests"),
        ("5. 服务器维护", "503 Service Unavailable"),
        ("6. 缓存数据", "304 Not Modified（配合缓存机制）"),
        ("7. 创建成功无内容", "204 No Content（DELETE 常用，POST 也可用）"),
        ("8. 重定向", "301 Moved Permanently（永久）或 302 Found（临时）"),
    ]
    for desc, answer in answers:
        print(f"  {desc} → {answer}")
    print()


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 49 - 字母异位词分组（Medium）
#    链接：https://leetcode.cn/problems/group-anagrams/
#    关联：今天学了 JSON 的键值对概念，这道题也是"分组"思维
#    思路提示：把排序后的字符串作为 dict 的 key，同组字符串放入 list
#
# 2. LeetCode 1 - 两数之和（Easy）
#    链接：https://leetcode.cn/problems/two-sum/
#    思路提示：用 dict 存 {target - num: index}，一次遍历搞定
#
# 💡 第 1 题是面试超高频题，务必掌握
# ============================================================


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    print("\n" + "🚀 " * 15)
    print("  Day 24 RESTful API 设计 - 练习开始")
    print("🚀 " * 15 + "\n")

    print("请选择要运行的练习：")
    print("  1 - 练习 1 答案：API 设计")
    print("  2 - 练习 2 答案：找茬修正")
    print("  3 - 练习 3：JSON 数据处理（编程）")
    print("  4 - 练习 4 答案：统一响应格式")
    print("  5 - 练习 5 答案：状态码选择")
    print("  0 - 退出")
    print()

    choice = input("输入编号：").strip()

    if choice == "1":
        check_exercise_1()
    elif choice == "2":
        check_exercise_2()
    elif choice == "3":
        exercise_3_json_practice()
    elif choice == "4":
        check_exercise_4()
    elif choice == "5":
        check_exercise_5()
    elif choice == "0":
        print("退出。")
    else:
        print("无效输入")
