import sys

sys.path.insert(0, ".")
from models import Base, User, Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///cascade_test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 插入一个用户和他的待办
u = User(username="test_user", hashed_password="pw")
db.add(u)
db.flush()
db.add_all(
    [
        Todo(title="待办A", user_id=u.id),
        Todo(title="待办B", user_id=u.id),
    ]
)
db.commit()
print(
    f"用户{u.username}有 {len(db.query(Todo).filter(Todo.user_id==u.id).all())} 条待办"
)

# 尝试删除用户
db.delete(u)
db.commit()  # 会发生什么？

# 检查剩余数据
remaining = db.query(User).all()
todo_count = db.query(Todo).count()
print(f"剩余用户数：{len(remaining)}, 剩余待办数：{todo_count}")

db.close()
