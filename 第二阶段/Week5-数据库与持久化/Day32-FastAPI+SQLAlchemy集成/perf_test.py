import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer, default=0)


engine = create_engine("sqlite:///perf_test.db", echo=False)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== 方法 1：逐条插入（慢）=====
db1 = SessionLocal()
start = time.perf_counter()
for i in range(1000):
    product = Product(name=f"商品{i}", price=i * 10)
    db1.add(product)  # 每次 add 只放入缓冲区
    db1.commit()  # 每次都提交！！！太慢了
elapsed1 = time.perf_counter() - start
print(f"方法1（逐条commit）：{elapsed1:.3f}秒")

# ===== 方法 2：批量加入 + 一次提交（快）=====
db2 = SessionLocal()
start = time.perf_counter()
products = [Product(name=f"商品{i}", price=i * 10) for i in range(1000)]
db2.add_all(products)  # 一次性加入所有对象
db2.commit()  # 一次提交搞定
elapsed2 = time.perf_counter() - start
print(f"方法2（add_all + 一次commit）：{elapsed2:.3f}秒")

# ===== 方法 3：flush + 一次 commit（最快）=====
db3 = SessionLocal()
start = time.perf_counter()
products = [Product(name=f"商品{i}", price=i * 10) for i in range(1000)]
db3.add_all(products)
db3.flush()  # 先 flush 到数据库
db3.commit()  # 再 commit 持久化
elapsed3 = time.perf_counter() - start
print(f"方法3（add_all + flush + commit）：{elapsed3:.3f}秒")

print(f"\n最慢的是方法1，快了约 {elapsed1/elapsed2:.1f} 倍")
db1.close()
db2.close()
db3.close()
