import sqlite3
from datetime import datetime

# 1. 连接SQLite数据库，改成你的数据库文件名
DB_FILE = "app.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 2. 准备测试数据：user_id, title, description, category, completed
todo_list = [
    # ========== test 用户 id=1 共8条 ==========
    (1, "晨起慢跑", "江边慢跑4公里，拉伸10分钟", "运动", 0),
    (1, "FastAPI刷题", "完成路由、依赖、分页练习", "学习", 1),
    (1, "超市买菜", "肉类、蔬果、饮用水采购", "日常", 0),
    (1, "洗衣服", "机洗全部外衣+内衣手洗", "家务", 1),
    (1, "看技术文档", "阅读SQLAlchemy2.0官方文档", "学习", 0),
    (1, "午休听歌", "轻音乐放松半小时", "休闲", 0),
    (1, "整理代码", "归类VSCode项目文件", "工作", 1),
    (1, "睡前读书", "看半小时课外书", "休闲", 0),
    # ========== xjx 用户 id=2 共6条 ==========
    (2, "数据库练习", "练习Alembic迁移、count分页", "学习", 0),
    (2, "拖地全屋", "客厅、卧室、阳台清扫拖地", "家务", 0),
    (2, "下午茶", "泡奶茶搭配小饼干", "生活", 1),
    (2, "吉他练习", "练习C、G、Am基础和弦", "爱好", 0),
    (2, "整理桌面", "收纳数据线、笔记本", "居家", 1),
    (2, "刷编程题", "LeetCode简单算法两道", "学习", 0),
]

# 3. 批量插入SQL
insert_sql = """
INSERT INTO todos (user_id, title, description, category, completed, created_at)
VALUES (?, ?, ?, ?, ?, ?)
"""
now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 循环插入
for item in todo_list:
    uid, title, desc, cate, finish = item
    cursor.execute(insert_sql, (uid, title, desc, cate, finish, now_time))

# 4. 提交保存、关闭连接
conn.commit()
print(f"成功插入 {len(todo_list)} 条待办记录！")
print(f"test(user=1) 8条，xjx(user=2) 6条")
conn.close()
