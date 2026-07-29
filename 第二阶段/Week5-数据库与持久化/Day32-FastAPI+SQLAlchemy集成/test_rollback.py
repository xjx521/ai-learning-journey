from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)


engine = create_engine(
    "sqlite:///rollback_test.db", echo=True
)  # echo=True，自动打印程序执行的全部原生 SQL 语句到控制台
Base.metadata.drop_all(bind=engine)  # 清理旧表
Base.metadata.create_all(bind=engine)  # 重新建表
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== 场景 1：正常 commit =====
print("=" * 50)
print("场景 1：正常提交")
db = SessionLocal()
item = Item(name="苹果")
db.add(item)
db.commit()  # ← 成功提交
db.refresh(item)
print(f"添加了：{item.name} (ID={item.id})")
db.close()

# ===== 场景 2：出错后 rollback =====
print("=" * 50)
print("场景 2：异常后回滚")
db = SessionLocal()
item1 = Item(name="香蕉")
db.add(item1)

item2 = Item(name=None)  # name 不允许为 NULL（模拟错误）
db.add(item2)

try:
    db.commit()  # ← 这里会报错
except Exception as e:
    print(f"出错了：{e}")
    db.rollback()  # ← 关键！回滚撤销刚才的操作
    print("已回滚，item1 和 item2 都没保存")

# 验证——看看数据库里有没有刚才的东西
db2 = SessionLocal()
remaining = db2.query(Item).all()
print(f"数据库剩余记录数：{len(remaining)}")
db2.close()

# ===== 场景 3：flush 但不 commit =====
print("=" * 50)
print("场景 3：flush 之后 rollback")
db = SessionLocal()
item3 = Item(name="橘子")
db.add(item3)
db.flush()  # ← 写入当前事务但不持久化
can_see = db.query(Item).count()
print(f"flush 后可见记录数：{can_see}")
db.rollback()  # ← 撤销
after_rollback = db.query(Item).count()
print(f"rollback 后可见记录数：{after_rollback}")
db.close()
