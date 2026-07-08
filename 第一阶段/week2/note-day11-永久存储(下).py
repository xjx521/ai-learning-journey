Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
 1. json.dumps / json.loads（字符串级别）
  import json

  # dump/load 是操作文件的
  json.dump(data, f)    # 写入文件
  data = json.load(f)   # 从文件读取

  # dumps/loads 是操作字符串的（多了个 s）
  json_str = json.dumps(data, ensure_ascii=False, indent=2)   # Python 对象 → JSON 字符串
  data = json.loads(json_str)                                  # JSON 字符串 → Python 对象
  为什么需要？ 调用 API（通义千问/OpenAI）时，请求和返回都是 JSON 字符串，不是文件，必须用 dumps/loads。

  2. Python 类型 ↔ JSON 类型对照

  ┌────────────┬────────┐
  │   Python   │  JSON  │
  ├────────────┼────────┤
  │ dict       │ object │
  ├────────────┼────────┤
  │ list/tuple │ array  │
  ├────────────┼────────┤
  │ str        │ string │
  ├────────────┼────────┤
  │ int/float  │ number │
  ├────────────┼────────┤
  │ True       │ true   │
  ├────────────┼────────┤
  │ False      │ false  │
  ├────────────┼────────┤
  │ None       │ null   │
  └────────────┴────────┘

  # 注意 tuple 会变成 array（失去元组特性）
  json.dumps((1, 2, 3))  # → "[1, 2, 3]"，读回来是 list 不是 tuple

  3. 常见应用场景
  # 保存/加载配置文件（AI 项目常用）
  config = {"api_key": "sk-xxx", "model": "qwen-turbo", "temperature": 0.7}
  with open("config.json", "w") as f:
      json.dump(config, f)

  with open("config.json") as f:
      config = json.load(f)
      print(config["model"])

  # API 返回的 JSON 字符串解析
  api_response = '{"choices": [{"message": {"content": "你好"}}]}'
  data = json.loads(api_response)
  print(data["choices"][0]["message"]["content"])  # → 你好

  4. 容错处理
  try:
      with open("data.json") as f:
          data = json.load(f)
  except json.JSONDecodeError as e:
      print(f"JSON 格式错误：{e}")
  except FileNotFoundError:
      print("文件不存在")

  ---
  二、文件操作补充（应该了解 ⭐⭐）

  1. 二进制文件模式（rb / wb）
  # 后续你做 RAG 系统时，要读取 PDF/图片 传给 AI 模型
  with open("image.png", "rb") as f:  # rb = read binary
      image_data = f.read()

  with open("model.bin", "wb") as f:  # wb = write binary
      f.write(model_bytes)
  和普通 r/w 的区别：r/w 按文本处理（会做编码转换），rb/wb
  按原始字节处理，不会修改任何内容。图片、音频、模型文件必须用二进制模式。

  2. os.path vs pathlib
  你的笔记记了 pathlib（新版推荐），但老项目大量用 os.path，要认识：
  import os
  os.path.join("week2", "data.pkl")        # 拼接路径 → "week2/data.pkl"
  os.path.exists("student.csv")            # 是否存在
  os.path.isfile("data.pkl")               # 是否文件
  os.path.isdir("week2")                   # 是否目录
  os.path.splitext("homework.py")          # → ("homework", ".py")

  ---
  三、pickle（需要知道风险 ⭐）

  你的笔记刚开了个头，补充关键点：

  import pickle

  # 存——保存任意 Python 对象
  with open("data.pkl", "wb") as f:       # 注意用 wb（二进制）
      pickle.dump({"name": "小明", "score": [85, 92, 78]}, f)

  # 取——恢复对象
  with open("data.pkl", "rb") as f:       # 注意用 rb
      data = pickle.load(f)
      print(data["score"])                # → [85, 92, 78]

 ## ⚠️ 重要警告：pickle 不要加载不信任来源的文件！它可以执行任意代码，有安全风险。只在"自己存自己读"的场景用。JSON 和 CSV
 ## 更安全，适合跨系统传输数据。

  ---
  ##总结：你需要额外学的

  ┌────────────────────────────┬────────┬───────────────────────────┐
  │           知识点           │ 优先级 │           原因            │
  ├────────────────────────────┼────────┼───────────────────────────┤
  │ JSON dumps/loads           │ ⭐⭐⭐ │ AI API 调用的核心技能     │
  ├────────────────────────────┼────────┼───────────────────────────┤
  │ JSON 容错处理              │ ⭐⭐⭐ │ 网络请求经常返回非法 JSON │
  ├────────────────────────────┼────────┼───────────────────────────┤
  │ 二进制文件 rb/wb           │ ⭐⭐   │ 读图片/PDF/模型文件必需   │
  ├────────────────────────────┼────────┼───────────────────────────┤
  │ os.path 认识               │ ⭐⭐   │ 老项目大量使用            │
  ├────────────────────────────┼────────┼───────────────────────────┤
  │ pickle 完整用法 + 安全风险 │ ⭐     │ 知道就行，谨慎使用        │
  └────────────────────────────┴────────┴───────────────────────────┘

  小甲鱼的课程侧重基础文件操作，实际 AI 开发中 80% 的数据交互都是 JSON。建议你把 JSON 的 dump/dumps/load/loads
  四件套练熟，后续调用 API 时自然就记住了。