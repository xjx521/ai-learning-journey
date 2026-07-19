"""
Day 22 练习题：HTTP 协议基础
==========================

⚠️ 注意：本练习需要安装 requests 库
    pip install requests

部分练习需要联网（访问 httpbin.org 等测试 API）
"""

import requests
import json

# ============================================================
# 【练习 1】URL 结构分析（笔答题，写在注释里）
# ============================================================
"""
请分析以下 URL 的各部分：
https://api.github.com:443/repos/octocat/Hello-World/issues?state=open&sort=created#comments

1. 协议（Scheme）：_____________
2. 域名（Host）：_____________
3. 端口（Port）：_____________
4. 路径（Path）：_____________
5. 查询参数（Query String）：_____________
6. 片段标识符（Fragment）：_____________

请写出你的答案后再运行本文件对照答案。
"""

# 练习 1 的答案
def check_exercise_1():
    answers = {
        "协议": "https",
        "域名": "api.github.com",
        "端口": "443",
        "路径": "/repos/octocat/Hello-World/issues",
        "查询参数": "state=open&sort=created",
        "片段标识符": "comments",
    }
    print("=" * 50)
    print("【练习 1 答案】URL 结构分析")
    print("=" * 50)
    for k, v in answers.items():
        print(f"  {k}：{v}")
    print()


# ============================================================
# 【练习 2】HTTP 方法选择（场景题）
# ============================================================
"""
场景：你在开发一个博客系统的 API，请为以下操作选择最合适的 HTTP 方法：

1. 用户查看文章列表 → _____
2. 用户发布新文章 → _____
3. 用户修改某篇文章的全部内容 → _____
4. 用户删除某篇文章 → _____
5. 用户只修改文章的标题（其他不变）→ _____
6. 用户搜索文章（带关键词参数）→ _____
"""

def check_exercise_2():
    answers = {
        "1. 查看文章列表": "GET",
        "2. 发布新文章": "POST",
        "3. 修改文章全部内容": "PUT",
        "4. 删除文章": "DELETE",
        "5. 只修改文章标题": "PATCH",
        "6. 搜索文章": "GET（参数放在查询字符串中）",
    }
    print("=" * 50)
    print("【练习 2 答案】HTTP 方法选择")
    print("=" * 50)
    for k, v in answers.items():
        print(f"  {k} → {v}")
    print()


# ============================================================
# 【练习 3】状态码判断
# ============================================================
"""
请为以下场景选择最合适的 HTTP 状态码：

1. 用户注册成功，账户已创建 → _____
2. 用户尝试登录，但密码错误 → _____
3. 用户访问一个不存在的页面 → _____
4. 用户未登录就访问需要登录的页面 → _____
5. 用户已登录但试图访问管理员专属页面 → _____
6. 服务器数据库连接失败，无法处理请求 → _____
7. 用户重复提交表单被限流 → _____
8. 请求成功，数据正常返回 → _____
9. 删除资源成功，不需要返回内容 → _____
10. 客户端发送的 JSON 格式不对 → _____
"""

def check_exercise_3():
    answers = {
        "1. 注册成功": "201 Created",
        "2. 密码错误": "401 Unauthorized",
        "3. 页面不存在": "404 Not Found",
        "4. 未登录": "401 Unauthorized",
        "5. 无权限": "403 Forbidden",
        "6. 数据库挂了": "500 Internal Server Error",
        "7. 被限流": "429 Too Many Requests",
        "8. 正常返回": "200 OK",
        "9. 删除成功": "204 No Content",
        "10. JSON 格式错误": "400 Bad Request",
    }
    print("=" * 50)
    print("【练习 3 答案】状态码判断")
    print("=" * 50)
    for k, v in answers.items():
        print(f"  {k} → {v}")
    print()


# ============================================================
# 【练习 4】用 requests 发送 GET 请求
# ============================================================
def exercise_4_get_request():
    """
    用 requests 库向 httpbin.org 发送 GET 请求
    httpbin.org 是一个 HTTP 测试网站，会返回你发送的请求信息
    """
    print("=" * 50)
    print("【练习 4】发送 GET 请求")
    print("=" * 50)

    # TODO 1：向 https://httpbin.org/get 发送 GET 请求
    # 带上查询参数：name=你的英文名, day=22
    # 提示：用 params 参数传字典
    url = "https://httpbin.org/get"
    params = {
        "name": "YourName",  # ← 改成你的英文名
        "day": 22,
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        # 打印关键信息
        print(f"请求 URL：{response.url}")
        print(f"状态码：{response.status_code}")
        print(f"响应 Content-Type：{response.headers.get('Content-Type')}")

        # 解析 JSON 响应
        data = response.json()
        print(f"服务器收到的参数：{data.get('args')}")
        print(f"你的 User-Agent：{data.get('headers', {}).get('User-Agent', 'N/A')[:50]}...")
        print("✅ GET 请求成功！\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败（检查网络连接）：{e}\n")


# ============================================================
# 【练习 5】用 requests 发送 POST 请求
# ============================================================
def exercise_5_post_request():
    """
    用 requests 库发送 POST 请求，模拟"创建用户"
    """
    print("=" * 50)
    print("【练习 5】发送 POST 请求")
    print("=" * 50)

    # TODO 2：向 https://httpbin.org/post 发送 POST 请求
    # 用 JSON 格式发送以下数据：
    # {"username": "你的名字", "age": 你的年龄, "email": "你的邮箱"}
    url = "https://httpbin.org/post"
    payload = {
        "username": "zhangsan",  # ← 改成你的信息
        "age": 21,
        "email": "zhangsan@example.com",
    }

    try:
        # 提示：用 json= 参数会自动设置 Content-Type 为 application/json
        response = requests.post(url, json=payload, timeout=10)

        print(f"状态码：{response.status_code}")
        data = response.json()

        # 验证服务器收到的数据
        received_data = data.get("json")
        print(f"服务器收到的 JSON 数据：{received_data}")
        print(f"请求的 Content-Type：{data.get('headers', {}).get('Content-Type')}")

        # 断言验证（自动检查你的请求是否正确）
        assert response.status_code == 200, "状态码应该是 200"
        assert received_data["username"] == payload["username"], "用户名应该匹配"
        print("✅ POST 请求成功，数据验证通过！\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}\n")
    except AssertionError as e:
        print(f"❌ 验证失败：{e}\n")


# ============================================================
# 【练习 6】观察请求头
# ============================================================
def exercise_6_headers():
    """
    学习设置自定义请求头
    """
    print("=" * 50)
    print("【练习 6】自定义请求头")
    print("=" * 50)

    # TODO 3：发送 GET 请求，带上自定义请求头
    # 要求：
    #   - Accept: application/json
    #   - X-Custom-Header: 你学号的后四位
    #   - Authorization: Bearer my-fake-token-123
    url = "https://httpbin.org/headers"
    headers = {
        "Accept": "application/json",
        "X-Custom-Header": "0000",  # ← 改成你学号后四位
        "Authorization": "Bearer my-fake-token-123",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        received_headers = data.get("headers", {})

        print("服务器收到的请求头：")
        for key in ["Accept", "X-Custom-Header", "Authorization"]:
            actual = received_headers.get(key, "❌ 未收到")
            expected = headers[key]
            status = "✅" if actual == expected else "❌"
            print(f"  {status} {key}: {actual}")

        print()

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}\n")


# ============================================================
# 【练习 7】状态码实战
# ============================================================
def exercise_7_status_codes():
    """
    用 httpbin.org 测试不同的状态码响应
    """
    print("=" * 50)
    print("【练习 7】体验不同状态码")
    print("=" * 50)

    # TODO 4：分别请求以下 URL，观察状态码
    test_urls = [
        ("https://httpbin.org/status/200", "成功"),
        ("https://httpbin.org/status/404", "未找到"),
        ("https://httpbin.org/status/500", "服务器错误"),
        ("https://httpbin.org/status/401", "未认证"),
        ("https://httpbin.org/status/301", "重定向（注意：requests 会自动跟随）"),
    ]

    for url, description in test_urls:
        try:
            # allow_redirects=False 可以阻止自动重定向，看到真实的 3xx 状态码
            response = requests.get(url, timeout=10, allow_redirects=False)
            print(f"  [{response.status_code}] {description}")
        except requests.exceptions.RequestException as e:
            print(f"  [ERR] {description} - {e}")

    print()


# ============================================================
# 【练习 8】综合：模拟 RESTful API 的完整 CRUD 操作
# ============================================================
def exercise_8_crud_simulation():
    """
    综合练习：用 JSONPlaceholder（假数据 API）模拟完整的增删改查
    https://jsonplaceholder.typicode.com/

    这个 API 支持真实的 CRUD 操作（但不会真正保存，返回模拟数据）
    """
    print("=" * 50)
    print("【练习 8】RESTful API 完整 CRUD 模拟")
    print("=" * 50)

    base_url = "https://jsonplaceholder.typicode.com"

    try:
        # --- 1. CREATE (POST) ---
        print("\n📝 1. 创建新帖子 (POST)")
        new_post = {
            "title": "我的 Day 22 学习心得",
            "body": "今天我学会了 HTTP 协议的基础知识！",
            "userId": 1,
        }
        response = requests.post(f"{base_url}/posts", json=new_post, timeout=10)
        print(f"   状态码：{response.status_code}（期望 201）")
        created = response.json()
        print(f"   返回数据：{json.dumps(created, ensure_ascii=False)}")
        post_id = created.get("id")

        # --- 2. READ (GET) ---
        print(f"\n📖 2. 获取帖子 (GET) - ID: {post_id}")
        response = requests.get(f"{base_url}/posts/{post_id}", timeout=10)
        print(f"   状态码：{response.status_code}（期望 200）")
        print(f"   返回数据：{json.dumps(response.json(), ensure_ascii=False)}")

        # --- 3. UPDATE (PUT) ---
        print(f"\n✏️ 3. 全量更新帖子 (PUT) - ID: {post_id}")
        updated_post = {
            "title": "我的 Day 22 学习心得（已更新）",
            "body": "HTTP 协议包括请求方法、状态码、请求头等核心概念。",
            "userId": 1,
            "id": post_id,
        }
        response = requests.put(f"{base_url}/posts/{post_id}", json=updated_post, timeout=10)
        print(f"   状态码：{response.status_code}（期望 200）")
        print(f"   返回数据：{json.dumps(response.json(), ensure_ascii=False)}")

        # --- 4. DELETE ---
        print(f"\n🗑️ 4. 删除帖子 (DELETE) - ID: {post_id}")
        response = requests.delete(f"{base_url}/posts/{post_id}", timeout=10)
        print(f"   状态码：{response.status_code}（期望 200）")

        # --- 5. 验证删除 ---
        print(f"\n🔍 5. 验证删除 (GET) - ID: {post_id}")
        response = requests.get(f"{base_url}/posts/{post_id}", timeout=10)
        print(f"   状态码：{response.status_code}")
        # 注意：JSONPlaceholder 删除后 GET 仍能返回（它是假删除），实际 API 通常返回 404

        print("\n✅ CRUD 操作全部完成！\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败（检查网络连接）：{e}\n")


# ============================================================
# 【练习 9】思考题
# ============================================================
"""
请思考以下问题，先自己写答案，再运行本文件查看参考答案：

1. 为什么 GET 请求的参数放在 URL 里，而 POST 放在 Body 里？
   这样设计有什么好处和限制？

2. 如果一个 API 接口既可以接受 GET 也可以接受 POST，
   你会怎么选择？有什么判断标准？

3. HTTP 是"无状态"的，但我们在网站上登录后却能保持登录状态。
   这是怎么做到的？你知道几种方案？

4. 401 Unauthorized 和 403 Forbidden 有什么区别？
   请举一个生活中的例子来类比。

5. 为什么刷新页面时，浏览器会警告"确认重新提交表单"？
   这和 HTTP 方法的哪个特性有关？
"""


# ==================== 参考答案 ====================
def check_exercise_9():
    print("=" * 50)
    print("【练习 9 参考答案】思考题")
    print("=" * 50)
    answers = [
        (
            "1. GET vs POST 参数位置",
            "GET 参数在 URL 中 → 可被缓存/收藏/分享，适合'查询'操作。\n"
            "   限制：URL 长度有限（~2048字符），且不安全（密码不应放URL）。\n"
            "   POST 参数在 Body 中 → 无长度限制，不会被缓存，适合'提交'操作。"
        ),
        (
            "2. GET 还是 POST？",
            "判断标准：\n"
            "   - 操作是否幂等？（多次执行结果一样 → GET）\n"
            "   - 参数是否敏感？（密码/个人信息 → POST）\n"
            "   - 参数量是否大？（超过 URL 限制 → POST）\n"
            "   - 是否需要缓存？（搜索结果可缓存 → GET）"
        ),
        (
            "3. 无状态的解决方案",
            "方案一：Cookie + Session → 服务器存 Session，客户端存 Cookie 中的 session_id\n"
            "   方案二：JWT Token → 服务器生成加密 Token，客户端存在 localStorage，\n"
            "   每次请求带上 Authorization: Bearer <token>\n"
            "   方案三：URL 重写 → 把 session_id 拼在 URL 里（不推荐，不安全）"
        ),
        (
            "4. 401 vs 403",
            "401 = '你是谁？' → 未认证（没登录/Token过期）\n"
            "   403 = '我知道你是谁，但你不行' → 已认证但无权限\n"
            "   生活例子：\n"
            "   401 = 你没有门禁卡，保安不让你进\n"
            "   403 = 你有门禁卡，但你的卡只能进大厅，进不了 VIP 室"
        ),
        (
            "5. 刷新表单警告",
            "因为 POST 请求不是幂等的。浏览器警告你：\n"
            "   '刷新会重新发送 POST 请求，可能导致重复提交（重复下单/重复付款）'\n"
            "   GET 请求刷新不会有这个警告，因为 GET 是幂等的，刷新只是重新获取数据。"
        ),
    ]
    for title, answer in answers:
        print(f"\n📌 {title}")
        print(f"   {answer}")
    print()


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 242 - 有效的字母异位词（Easy）
#    链接：https://leetcode.cn/problems/valid-anagram/
#    关联：今天学了 HTTP 的"请求-响应"配对概念，这道题也是"配对"思维
#    思路提示：用 collections.Counter 统计字符频次，比较两个 Counter 是否相等
#
# 2. LeetCode 20 - 有效的括号（Easy）
#    链接：https://leetcode.cn/problems/valid-parentheses/
#    思路提示：用栈（list 即可），左括号入栈，右括号弹出栈顶检查匹配
#    注意：最后栈应为空
#
# 💡 建议：先自己想 15 分钟，实在不会再看题解
# ============================================================


# ============================================================
# 主程序：运行所有练习
# ============================================================
if __name__ == "__main__":
    print("\n" + "🚀 " * 15)
    print("  Day 22 HTTP 协议基础 - 练习开始")
    print("🚀 " * 15 + "\n")

    # 笔答题答案
    check_exercise_1()
    check_exercise_2()
    check_exercise_3()

    # 编程练习（需要联网）
    print("⚠️  以下练习需要联网，如果超时请检查网络或代理设置\n")
    exercise_4_get_request()
    exercise_5_post_request()
    exercise_6_headers()
    exercise_7_status_codes()
    exercise_8_crud_simulation()

    # 思考题参考答案
    check_exercise_9()

    print("=" * 50)
    print("🎉 所有练习运行完毕！")
    print("📌 别忘了做今天的 LeetCode 推荐题！")
    print("=" * 50)
