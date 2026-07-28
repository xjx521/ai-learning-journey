"""
Day 31 练习题：Alembic 数据库迁移 + 数据库设计
================================================

⚠️ 前置准备：
    pip install sqlalchemy alembic

💡 建议：每个实验在独立目录中测试，避免 Alembic 命令冲突（alembic init 只在项目根目录执行一次）。
完成每一个「测试」和「问题」后再翻到文件末尾的参考答案。
"""

import os, sys, subprocess, shutil, json, sqlite3, time
from pathlib import Path

# ============================================================
# 【实验 1】初始化 Alembic + 自动生成迁移
# ============================================================
"""
目标：理解 alembic init + autogenerate 的工作流程

步骤：找一个空目录，逐步完成以下操作：

```bash
# 1. 创建并进入实验目录
mkdir day31_exp1 && cd day31_exp1

# 2. 先安装依赖
pip install sqlalchemy alembic

# 3. 写一个简单的模型文件 models.py
```

```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
```

```bash
# 4. 初始化 Alembic
alembic init alembic

# 5. 修改 env.py 中的 target_metadata（添加导入 + 赋值）
# 6. 修改 alembic.ini 的 sqlalchemy.url
#     sqlite:///./exp1.db

# 7. 生成迁移脚本
alembic revision --autogenerate -m "create users table"

# 8. 检查生成的文件
cat alembic/versions/xxxx_create_users_table.py

# 9. 执行迁移
alembic upgrade head

# 10. 验证数据库
sqlite3 exp1.db ".schema users"
```

❓ **问题 1.1**：为什么需要先写 models.py 再运行 `alembic revision`？
要先有模型类确认数据库表里的内容才能进行迁移
❓ **问题 1.2**：`alembic init` 只能执行一次吗？重复执行会怎样？
重复执行会报错：alembic已存在里面非空
❓ **问题 1.3**：env.py 里为什么要加 `sys.path.insert()`？不加会发生什么报错？
会找不到文件ModuleNotFoundError: No module named 'models'。
"""


def run_experiment_1():
    """完整演示实验 1 的所有步骤"""
    print("=" * 60)
    print("【实验 1】Alembic 初始化 + 自动生成迁移")
    print("=" * 60)

    exp_dir = Path("day31_exp1")
    if exp_dir.exists():
        shutil.rmtree(exp_dir)
    exp_dir.mkdir()

    # --- 写入 models.py ---
    (exp_dir / "models.py").write_text("""\
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
""")

    # --- 执行 alembic init ---
    result = subprocess.run(
        ["alembic", "init", "alembic"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"alembic init 返回码: {result.returncode}")
    print(f"成功创建了 alembic/ 文件夹")

    # --- 修改 alembic.ini ---
    ini_path = exp_dir / "alembic.ini"
    content = ini_path.read_text()
    content = content.replace(
        "sqlalchemy.url = driver://user:pass@localhost/dbname",
        "sqlalchemy.url = sqlite:///./exp1.db",
    )
    ini_path.write_text(content)
    print("已修改 alembic.ini 的 sqlalchemy.url")

    # --- 修改 env.py ---
    env_path = exp_dir / "alembic" / "env.py"
    code = env_path.read_text()

    # 添加 sys.path 和 models 导入
    imports_section = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from models import Base   # ← 导入你的 Base 类
"""
    code = code.replace(
        "target_metadata = None", f"target_metadata = Base.metadata{imports_section}"
    )

    # 取消注释 connection 部分
    code = code.replace(
        "# with connectable.connect() as connection:",
        "with connectable.connect() as connection:",
    )
    code = code.replace(
        "        # context.run_migrations(connection)",
        "        context.run_migrations(connection)",
    )
    env_path.write_text(code)
    print("已修改 env.py（导入 Base + 取消注释 connection）")

    # --- 生成迁移脚本 ---
    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", "create users table"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"alembic revision --autogenerate 返回码: {result.returncode}")
    if result.stderr:
        print(f"stderr: {result.stderr.strip()}")

    # --- 显示生成的迁移脚本内容 ---
    versions_dir = exp_dir / "alembic" / "versions"
    py_files = list(versions_dir.glob("*.py"))
    if py_files:
        latest = sorted(py_files)[-1]
        print(f"\n=== 生成的迁移脚本: {latest.name} ===")
        print(latest.read_text())

    # --- 执行迁移 ---
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"\nalembic upgrade head 返回码: {result.returncode}")

    # --- 验证 ---
    db_file = exp_dir / "exp1.db"
    if db_file.exists():
        print(f"数据库文件已创建: {db_file.absolute()}")
        # 用 sqlite3 查看表结构
        ver_result = subprocess.run(
            ["sqlite3", "exp1.db", ".schema users"],
            cwd=exp_dir,
            capture_output=True,
            text=True,
        )
        print(f"\n=== users 表结构 ===\n{ver_result.stdout.strip()}")

    print("\n✅ 实验 1 完成！")
    print("=" * 60)


# ============================================================
# 【实验 2】修改模型 → autogenerate → upgrade（增删列）
# ============================================================
"""
目标：体验完整的「改模型 → 生成迁移 → 应用迁移」工作流

步骤：在上一个实验的基础上继续操作。

先在 models.py 中添加新字段：

```python
# 在 User 类中新增两个字段
last_login = Column(String(50), nullable=True)       # 上次登录时间
role = Column(String(20), default="user")             # 用户角色（admin/user/guest）
```

然后执行：

```bash
# 1. 重新生成迁移（检测到模型变化了）
alembic revision --autogenerate -m "add last_login and role columns"

# 2. 查看生成的脚本——注意看里面是 ADD COLUMN 还是 CREATE TABLE
# 3. 执行迁移
alembic upgrade head

# 4. 验证新列是否存在
sqlite3 exp1.db "PRAGMA table_info(users);"
```

❓ **问题 2.1**：第二次 autogenerate 生成的脚本内容是什么样的？和第一次有什么区别？
upgrade 里面为pass 第一次有生成字段
第二次生成的是 ALTER TABLE ... ADD COLUMN last_login 和 ADD COLUMN role。
      而第一次是 CREATE TABLE users。ALTER 比 CREATE 简单多了，这就是增量迁移的优势。
❓ **问题 2.2**：如果我把已有的 username 字段的 String(50) 改成 String(100)，
         autogenerate 能自动检测到吗？生成的脚本会怎么写？
能检测到变化，但SQLite不支持直接修改列类型，Alembic会生成复杂的"重建表"脚本：
创建临时表→拷贝数据→删旧表→重命名临时表。这个过程容易出问题（数据类型不兼容等）。
💡 **破坏性实验：** 把 models.py 中的 `is_active` 字段整个删掉，然后运行 autogenerate ——
看看生成的 downgrade 函数做了什么（它是 DROP COLUMN 还是做不了？）。
执行DropcCOLUMN 删除is_actice
"""


def run_experiment_2():
    """完整演示实验 2 的流程"""
    print("\n" + "=" * 60)
    print("【实验 2】修改模型 → autogenerate → upgrade")
    print("=" * 60)

    exp_dir = Path("day31_exp1")

    # --- 第一步：先确认当前状态（只有 base 迁移） ---
    print("--- 当前迁移链状态 ---")
    result = subprocess.run(
        ["alembic", "history"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(result.stdout)

    # --- 第二步：修改 models.py，增加新字段 ---
    models = exp_dir / "models.py"
    new_models = models.read_text().replace(
        "is_active = Column(Boolean, default=True)\n",
        """is_active = Column(Boolean, default=True)
    last_login = Column(String(50), nullable=True)
    role = Column(String(20), default="user")
""",
    )
    models.write_text(new_models)
    print("\n--- 修改了 models.py，添加了 last_login 和 role 字段 ---")

    # --- 第三步：生成迁移脚本 ---
    result = subprocess.run(
        [
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            "add last_login and role columns",
        ],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"autogenerate 返回码: {result.returncode}")

    # --- 显示新生成的迁移脚本 ---
    versions_dir = exp_dir / "alembic" / "versions"
    py_files = sorted(versions_dir.glob("*.py"))
    if len(py_files) >= 2:
        latest = py_files[-1]
        print(f"\n=== 新增的迁移脚本 ({latest.name}) ===")
        print(latest.read_text())

    # --- 第四步：执行迁移 ---
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"upgrade head 返回码: {result.returncode}")

    # --- 第五步：验证 ---
    pragma_result = subprocess.run(
        ["sqlite3", "exp1.db", "PRAGMA table_info(users);"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"\n=== 修改后的 users 表结构 ===\n{pragma_result.stdout.strip()}")

    print("\n✅ 实验 2 完成！注意观察 migration chain 新增了哪个版本")
    print("=" * 60)


# ============================================================
# 【实验 3】downgrade 回滚迁移
# ============================================================
"""
目标：理解升级、降级、迁移链的概念

步骤：接上一个实验，继续操作。

首先查看当前状态：

```bash
# 1. 查看所有迁移历史
alembic history

# 2. 查看当前数据库处于哪个版本
alembic current
# 假设输出：002_add_last_login_and_role... (head)

# 3. 回退一步
alembic downgrade -1

# 4. 再看看当前版本和表结构
alembic current
sqlite3 exp1.db "PRAGMA table_info(users);"
# 现在 last_login 和 role 列应该消失了！

# 5. 再次升级回最新
alembic upgrade head

# 6. 也可以一步到位：从 base 到 head
alembic downgrade base   # 所有表都没了
alembic upgrade head     # 重建所有表
```

❓ **问题 3.1**：downgrade -1 之后，这个版本的数据（刚插入的用户记录）还在吗？
要分情况：如果只是 DROP COLUMN（删除某列），其他列的数据还在，但被删的那列数据丢失。
如果是 DROP TABLE（downgrade base 回到最初），整张表和数据全没了。
❓ **问题 3.2**：如果数据库已经有很多生产数据了，downgrade 会有什么问题？
如果 downgrade 删除了某列，那这列上的所有数据都会丢失且不可恢复。
      所以生产环境一定要先备份数据库再做 downgrade，或者改用 ADD COLUMN（只增不改）的策略。

💡 **破坏性实验：**
```bash
# 故意搞乱版本标记（不是真的 downgrading，只是改版本号）
alembic stamp head
alembic downgrade base
alembic upgrade head
```
这会强制设置版本号而不执行真正的迁移脚本，可以用来修复被误操作的迁移状态。
"""


def run_experiment_3():
    """完整演示实验 3 的升级和降级流程"""
    print("\n" + "=" * 60)
    print("【实验 3】downgrade 回滚迁移")
    print("=" * 60)

    exp_dir = Path("day31_exp1")

    # --- 先看当前状态 ---
    print("--- 当前迁移链 ---")
    result = subprocess.run(
        ["alembic", "history"], cwd=exp_dir, capture_output=True, text=True
    )
    print(result.stdout)

    result = subprocess.run(
        ["alembic", "current"], cwd=exp_dir, capture_output=True, text=True
    )
    current_ver = result.stdout.strip()
    print(f"当前版本: {current_ver}")

    # --- 先确保在 head ---
    subprocess.run(
        ["alembic", "upgrade", "head"], cwd=exp_dir, capture_output=True, text=True
    )

    # --- 查看表结构（有 last_login 和 role）---
    before = subprocess.run(
        ["sqlite3", "exp1.db", "PRAGMA table_info(users);"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"\n--- downgrade 之前的表结构 ---\n{before.stdout.strip()}")

    # --- downgrade -1 ---
    print("\n>>> 执行 alembic downgrade -1")
    subprocess.run(
        ["alembic", "downgrade", "-1"], cwd=exp_dir, capture_output=True, text=True
    )

    result = subprocess.run(
        ["alembic", "current"], cwd=exp_dir, capture_output=True, text=True
    )
    print(f"降级后版本: {result.stdout.strip()}")

    after = subprocess.run(
        ["sqlite3", "exp1.db", "PRAGMA table_info(users);"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"\n--- downgrade -1 之后的表结构 ---\n{after.stdout.strip()}")
    print("(注意 last_login 和 role 列消失了)")

    # --- 升级回 head ---
    print("\n>>> 执行 alembic upgrade head")
    subprocess.run(
        ["alembic", "upgrade", "head"], cwd=exp_dir, capture_output=True, text=True
    )

    restored = subprocess.run(
        ["sqlite3", "exp1.db", "PRAGMA table_info(users);"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"\n--- upgrade back 之后的表结构 ---\n{restored.stdout.strip()}")

    # --- 演示 base → head 完整流程 ---
    print("\n\n>>> 演示从 base 重建所有表:")
    subprocess.run(
        ["alembic", "downgrade", "base"], cwd=exp_dir, capture_output=True, text=True
    )
    tables_after_base = subprocess.run(
        ["sqlite3", "exp1.db", ".tables"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"downgrade base 后剩余表: {tables_after_base.stdout.strip()}")

    subprocess.run(
        ["alembic", "upgrade", "head"], cwd=exp_dir, capture_output=True, text=True
    )
    tables_after_upgrade = subprocess.run(
        ["sqlite3", "exp1.db", ".tables"],
        cwd=exp_dir,
        capture_output=True,
        text=True,
    )
    print(f"upgrade head 后剩余表: {tables_after_upgrade.stdout.strip()}")

    print("\n✅ 实验 3 完成！理解了 upgrade/downgrade 对表结构的实际影响")
    print("=" * 60)


# ============================================================
# 【实验 4】范式判断练习
# ============================================================
"""
目标：通过具体例子判断表的范式级别，理解何时拆分、何时冗余

请判断以下每个表的范式级别，并说明理由：

----------------------------------------------------------------
表A（student_id, course_id, student_name, grade）
- 主键：(student_id, course_id) — 复合主键
- student_name 只依赖于 student_id，grade 依赖于 (student_id, course_id) 组合
----------------------------------------------------------------

❓ **问题 4-A.1**：这是第几范式？违反了哪一范式的规则？
答：____________违反了第二范式__2NF 应该建学生表(student_id,student_name)____student_name依赖于student_id____________________________________
____和成绩表(course_id,grade)grade依赖于course_id为主键____________________________________________________________

----------------------------------------------------------------
表B（order_id, customer_id, customer_name, order_date, total_amount）
- 主键：order_id（单列主键）
- customer_name 依赖于 customer_id 而不依赖于 order_id
----------------------------------------------------------------

❓ **问题 4-B.1**：这是第几范式？有没有优化空间？
答：___3NF（违反第三范式）___主键order_id是单列不存在部分依赖所以2NF满足。但customer_name通过customer_id传递依赖主键(order_id→customer_id→customer_name)，这是传递依赖违反3NF。
________拆分为：订单表(order_id, customer_id, order_date, total_amount) + 顾客表(customer_id, customer_name)

----------------------------------------------------------------
表C（emp_id, name, dept_id, dept_name, dept_location）
- 主键：emp_id
- dept_name 和 dept_location 都依赖于 dept_id，dept_id 又依赖于 emp_id
----------------------------------------------------------------

❓ **问题 4-C.1**：这是第几范式？怎么拆分？
答：_____3NF（违反第三范式）✅ 你的答案正确！emp_id→dept_id→dept_name/dept_location 是传递依赖。
______________拆分：员工表(emp_id, name, dept_id) + 部门表(dept_id, dept_name, dept_location)

----------------------------------------------------------------
表D（product_id, product_name, price）
- 主键：product_id
- 没有外键，没有关联，最简单的商品表
----------------------------------------------------------------

❓ **问题 4-D.1**：这张表符合哪些范式？
答：_____ "表D 满足 1NF / 2NF / 3NF（甚至 4NF、5NF）！",
            "最简单的理想设计：单列主键、每列原子化、无部分依赖、无传递依赖。"
            "这种表叫 Entity Table（实体表），是规范化的典范。"_________________________________________________
________________________________________________________________
"""


def check_pandect_answers():
    """显示实验 4 的参考答案"""
    print("\n" + "=" * 60)
    print("【实验 4】范式判断参考答案")
    print("=" * 60)

    answers = [
        (
            "4-A",
            "表A 违反 2NF！",
            "主键是 (student_id, course_id)，但 student_name 只依赖 student_id（主键的一部分），"
            "这就是部分依赖。应拆分为两张表：学生表(student_id, student_name) + 选课成绩表(student_id, course_id, grade)。",
        ),
        (
            "4-B",
            "表B 违反 2NF！",
            "虽然主键是单列 order_id，但 customer_name 本质上与 customer_id 绑定。"
            "更好的设计是拆成订单表(order_id, customer_id, order_date, total_amount) + 客户表(customer_id, customer_name)，"
            "否则修改客户名字需要更新多条订单记录（更新异常）。",
        ),
        (
            "4-C",
            "表C 违反 3NF！",
            "存在传递依赖：emp_id → dept_id → dept_name → dept_location。"
            "非主键列 dept_name 不直接依赖主键 emp_id，而是通过 dept_id 间接依赖。"
            "拆分为员工表(emp_id, name, dept_id) + 部门表(dept_id, dept_name, dept_location)。",
        ),
        (
            "4-D",
            "表D 满足 1NF / 2NF / 3NF（甚至 4NF、5NF）！",
            "最简单的理想设计：单列主键、每列原子化、无部分依赖、无传递依赖。"
            "这种表叫 Entity Table（实体表），是规范化的典范。",
        ),
    ]

    for label, answer in answers:
        print(f"\n{'─' * 50}")
        print(f"问题 {label} 的参考答案：")
        print(f"  {answer}")

    print("\n" + "=" * 60)


run_experiment_1()
check_pandect_answers()


# ============================================================
# 【实验 5】索引实验（EXPLAIN ANALYZE 对比加索引前后）
# ============================================================
"""
目标：直观感受索引对查询性能的影响

步骤：用 Python sqlite3 模块创建一个带数据的数据库，然后对比加索引前后的查询速度：

```python
import sqlite3
import time

conn = sqlite3.connect("index_test.db")
c = conn.cursor()

# 创建一张大表（模拟真实场景）
c.execute('''
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT,
        content TEXT,
        created_at TEXT
    )
''')

# 批量插入 10000 条数据
categories = ["技术", "生活", "学习", "工作", "娱乐"]
for i in range(10000):
    c.execute(
        "INSERT INTO articles (title, category, content, created_at) VALUES (?, ?, ?, ?)",
        (f"文章第{i}篇", categories[i % 5], "这是一段示例内容" * 100, "2026-01-01")
    )
conn.commit()

# --- 不加索引，测一次查询 ---
start = time.perf_counter()
for _ in range(10):
    c.execute("SELECT * FROM articles WHERE category = ?", ("技术",))
    c.fetchall()
elapsed_no_index = (time.perf_counter() - start) / 10
print(f"不加索引的平均查询时间: {elapsed_no_index*1000:.2f} ms")

# --- 加上索引再测 ---
c.execute("CREATE INDEX idx_category ON articles(category)")
conn.commit()

start = time.perf_counter()
for _ in range(10):
    c.execute("SELECT * FROM articles WHERE category = ?", ("技术",))
    c.fetchall()
elapsed_with_index = (time.perf_counter() - start) / 10
print(f"加索引后的平均查询时间: {elapsed_with_index*1000:.2f} ms")

# --- 对比 ---
speedup = elapsed_no_index / elapsed_with_index if elapsed_with_index > 0 else float('inf')
print(f"加速比: {speedup:.2f}x")

conn.close()
```

❓ **问题 5.1**：加了索引后查询变快了多少倍？你的实测数据是多少？
加索引后的平均查询时间: 11.78 ms 不加索引的平均查询时间: 24.34 ms 快了两倍多
❓ **问题 5.2**：如果我对 created_at 也建了索引，但查询条件是
         `WHERE category = ? ORDER BY created_at DESC`，
         能不能只用一个索引同时搞定过滤和排序？为什么？
能 复合索引 做到边过滤边排序
💡 **破坏性实验：**
创建复合索引后，尝试不同的 WHERE 条件来观察是否使用索引：

```sql
-- 先创建复合索引
CREATE INDEX idx_cat_created ON articles(category, created_at);

-- ✅ 可以用索引
SELECT * FROM articles WHERE category = '技术';

-- ✅ 可以用索引
SELECT * FROM articles WHERE category = '技术' ORDER BY created_at DESC;

-- ❌ 不能用索引的前半部分
SELECT * FROM articles WHERE created_at > '2026-06-01';
```

思考：为什么复合索引要遵循最左前缀原则？如果不遵守会怎样？
答：___________  如果不遵守最左前缀（例如直接查 created_at），索引前半部分就无法利用，等于白建。___________________________________________
"""


def run_experiment_5():
    """完整演示实验 5 的索引性能对比"""
    print("\n" + "=" * 60)
    print("【实验 5】索引性能对比实验")
    print("=" * 60)

    db_path = "index_test.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 建表
    c.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    # 插入 10000 条数据
    print("正在插入 10000 条测试数据...")
    categories = ["技术", "生活", "学习", "工作", "娱乐"]
    data = [
        (f"文章第{i}篇", categories[i % 5], "示例内容" * 100, "2026-01-01")
        for i in range(10000)
    ]
    c.executemany(
        "INSERT INTO articles (title, category, content, created_at) VALUES (?, ?, ?, ?)",
        data,
    )
    conn.commit()
    print("数据插入完成！")

    # --- 不加索引 ---
    print("\n--- 不加索引：查询 10 次取平均 ---")
    start = time.perf_counter()
    for _ in range(10):
        c.execute("SELECT * FROM articles WHERE category = ?", ("技术",))
        c.fetchall()
    no_index_avg = (time.perf_counter() - start) / 10 * 1000
    print(f"平均查询时间: {no_index_avg:.2f} ms")

    # --- EXPLAIN 看没有索引时的执行计划 ---
    explain_no_idx = c.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM articles WHERE category = ?", ("技术",)
    ).fetchall()
    print(f"执行计划: {[row[3] for row in explain_no_idx]}")
    # 通常显示 "SCAN TABLE articles"（全表扫描）

    # --- 加索引 ---
    c.execute("CREATE INDEX idx_category ON articles(category)")
    conn.commit()

    print("\n--- 加索引后：查询 10 次取平均 ---")
    start = time.perf_counter()
    for _ in range(10):
        c.execute("SELECT * FROM articles WHERE category = ?", ("技术",))
        c.fetchall()
    with_index_avg = (time.perf_counter() - start) / 10 * 1000
    print(f"平均查询时间: {with_index_avg:.2f} ms")

    # --- EXPLAIN 看有索引时的执行计划 ---
    explain_with_idx = c.execute(
        "SELECT * FROM articles WHERE category = ?", ("技术",)
    ).fetchall()
    print(f"执行计划: {[row[3] for row in explain_with_idx]}")
    # 通常显示 "SEARCH TABLE articles USING INDEX ..."（走索引）

    # --- 对比 ---
    if with_index_avg > 0:
        speedup = no_index_avg / with_index_avg
        print(f"\n📊 加速比: {speedup:.2f}x （加索引后快了 {speedup:.1f} 倍）")
    else:
        print("\n📊 加索引后查询极快，几乎不需要时间")

    conn.close()
    os.remove(db_path)

    print("\n✅ 实验 5 完成！")
    print("关键发现：小表时差异不大，数据量越大索引优势越明显")
    print("但也别忘了：索引会增加 INSERT/UPDATE 的开销，不要对所有列都加索引！")
    print("=" * 60)


run_experiment_5()


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 217 - 存在重复元素（Easy）
#    链接：https://leetcode.cn/problems/contains-duplicate/
#    思路提示：用 set() 去重，如果去重后长度变小就说明有重复。对应数据库的唯一索引（UNIQUE constraint）概念
#
# 2. LeetCode 268 - 缺失的数字（Easy）
#    链接：https://leetcode.cn/problems/missing-number/
#    思路提示：数组索引天然对应数字，类似数据库的主键自增逻辑——如果有缺失，就是"断裂的 ID"
#
# 💡 唯一索引就是保证某列数据不重复——set() 的本质就是哈希去重，和数据库 UNIQUE 约束异曲同工
# ============================================================


# ============================================================
# 💡 参考答案（完成所有练习后再看！）
# ============================================================
# 🔑 使用说明：先独立做完上面所有【测试】和【问题】，再打开这里对照。
# 如果你的答案思路接近就算对，不必文字完全一致。
# ------------------------------------------------------------

"""
== 实验 1 参考答案 ==

问题 1.1：Alembic 需要读取 SQLAlchemy 模型类来对比当前数据库状态。如果没有 models.py，
      Alembic 就不知道你的表应该长什么样，无法生成差异脚本。
问题 1.2：是的，只能一次。再次执行会报 "Alembic directory already exists" 错误。
      如果需要重新初始化，必须先删除旧目录再 init。
问题 1.3：因为 env.py 在一个子目录 alembic/ 里运行时，Python 找不到父目录下的 models.py。
      不加会报 ModuleNotFoundError: No module named 'models'。


== 实验 2 参考答案 ==

问题 2.1：第二次生成的是 ALTER TABLE ... ADD COLUMN last_login 和 ADD COLUMN role。
      而第一次是 CREATE TABLE users。ALTER 比 CREATE 简单多了，这就是增量迁移的优势。
问题 2.2：SQLite 不支持直接修改列类型！Alembic 会生成一个复杂的脚本来重建表
      （拷贝→删旧→建新→恢复数据），但这容易出问题（比如数据类型不兼容）。
      所以很多 ORM 框架建议你手动处理这类修改。


== 实验 3 参考答案 ==

问题 3.1：在。downgrade 只是执行反向 SQL（如 ALTER TABLE DROP COLUMN），它不会删除表中已有的行数据。
      但如果你 downgrade 了一个包含 CREATE TABLE 的版本（base → 第一步），那整张表都没了，数据自然也没了。
问题 3.2：如果 downgrade 删除了某列，那这列上的所有数据都会丢失且不可恢复。
      所以生产环境一定要先备份数据库再做 downgrade，或者改用 ADD COLUMN（只增不改）的策略。


== 实验 4 参考答案 ==

问题 4-A.1：违反 2NF。主键是 (student_id, course_id)，但 student_name 只依赖 student_id（主键的一部分），
      这就是部分依赖。应拆分为两张表：学生表(student_id, student_name) + 选课成绩表(student_id, course_id, grade)。
问题 4-B.1：违反 2NF。虽然主键是单列 order_id，但 customer_name 本质上与 customer_id 绑定。
      更好的设计是拆成订单表(order_id, customer_id, order_date, total_amount) + 客户表(customer_id, customer_name)。
问题 4-C.1：违反 3NF。存在传递依赖：emp_id → dept_id → dept_name → dept_location。
      非主键列 dept_name 不直接依赖主键 emp_id，而是通过 dept_id 间接依赖。
      拆分为员工表(emp_id, name, dept_id) + 部门表(dept_id, dept_name, dept_location)。
问题 4-D.1：满足 1NF / 2NF / 3NF（甚至 4NF、5NF）！单列主键、每列原子化、无部分依赖、无传递依赖。
      这种表叫 Entity Table（实体表），是规范化的典范。


== 实验 5 参考答案 ==

问题 5.1：你的实测数据是多少？一般小表不明显，10000+ 条数据时差距开始显著（可能几倍到几十倍）。
问题 5.2：可以。复合索引 (category, created_at) 遵循最左前缀原则——第一个字段用于等值匹配，
      第二个字段用于排序。所以既能过滤又能排序，只用这一个索引就够了。
      如果不遵守最左前缀（例如直接查 created_at），索引前半部分就无法利用，等于白建。

== LeetCode 思路 ==

LC 217：遍历一次计数，O(n) 时间和 O(n) 空间。类似数据库 COUNT(GROUP BY) 找唯一值。
LC 268：排序后比较索引和值，或者用集合差集。range(len(nums)) 应该包含 0~n，缺的就是缺失的数字。
"""


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 31 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：Alembic 初始化 + 自动生成迁移脚本
[ ] 实验 2：修改模型 → autogenerate → upgrade（增量迁移）
[ ] 实验 3：downgrade 回滚迁移
[ ] 实验 4：范式判断练习（1NF / 2NF / 3NF）
[ ] 实验 5：索引性能对比实验（EXPLAIN ANALYZE）

遇到的问题：
______________________________________________________________
______________________________________________________________

学到的最重要的一点：
______________________________________________________________
______________________________________________________________
"""
