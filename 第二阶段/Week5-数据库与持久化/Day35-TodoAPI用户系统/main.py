from collections import Counter
from datetime import datetime, timedelta
import math
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
    select,
)
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, relationship
from fastapi import Depends, FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import os
import uvicorn

app = FastAPI(title="待办事项API", description="Day 35 综合项目", version="2.0.0")
load_dotenv()  # ← 加载 .env 文件

# **添加 CORS 中间件：**
allowed = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ========== 数据库配置 ==========
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)


# ========== 模型定义 ==========
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    todos = relationship("Todo", back_populates="owner", cascade="all,delete-orphan")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    category = Column(String, default="未分类", index=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="todos")


# 建表
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as err:
        db.rollback()
        raise err
    finally:
        db.close()


#### 2.1 POST /auth/register（注册）
pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


@app.post("/auth/register", status_code=201, tags=["用户中心"], summary="用户注册")
def register(user: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 1. 检查用户名是否已存在
    existing = db.execute(select(User).where(User.username == user.username)).scalar()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已被注册")

    # 2. 哈希密码
    hashed = pwd_context.hash(user.password)

    # 3. 创建用户
    new_user = User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "注册成功", "user_id": new_user.id}


#### 2.2 POST /auth/login（登录）

# 告诉框架去哪里拿token
OAuth2Schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 创建token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )  # jwt.encode 作用接收载荷字典、密钥、加密算法 payload=to_encode  常用键 SECRET_KEY对称加密，加密解密同一个密钥。生产务必放环境变量，不要写死代码上传 Git。 algorithm绝大多数业务固定 HS256，加密和解密算法必须一模一样


@app.post("/auth/login", tags=["用户中心"], summary="用户登录")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """用户登录"""
    # Annotated 把类型和依赖规则写在一起 OAuth2PasswordRequestForm 限定前端必须以from-data形式提交 Depends依赖注入
    # 1. 查用户
    user = db.execute(select(User).where(User.username == form_data.username)).scalar()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 2. 签发 token
    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


### Step 3 🔲 Bearer Token 鉴权


def get_current_user(
    token: Annotated[str, Depends(OAuth2Schema)], db: Session = Depends(get_db)
) -> User:
    """从 Bearer Token 中提取用户信息"""
    credentials_exception = HTTPException(
        status_code=401, detail="无法验证凭据", headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )  # jwt.decode：用来解析 token 拿 payload，入参顺序：decode(token字符串, 密钥, algorithms=[算法])algorithms复数
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except JWTError:
        raise credentials_exception
    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user


@app.get("/todos/me", tags=["待办事项"], summary="查看我的待办")
def list_my_todos(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10,
):
    """查看我的待办信息"""
    # current_user 就是当前登录的用户！
    todos = (
        db.execute(
            select(Todo)
            .where(Todo.user_id == current_user.id)
            .offset((page - 1) * size)
            .limit(size)
        )
        .scalars()
        .all()
    )  # .scalars() 必须写在 db.execute() 之后，不能拼接在 select 查询链末尾。
    total = db.execute(
        select(func.count(Todo.id)).where(Todo.user_id == current_user.id)
    ).scalar()

    return {
        "data": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
            }
            for t in todos
        ],
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size),
        },
    }


### Step 4 🔲 Todo CRUD 绑定 user_id
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    category: str
    completed: bool
    user_id: int  # ← 新增
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    category: str = "未分类"


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    completed: bool | None = None


# POST /todos（创建）
@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=201,
    tags=["待办事项"],
    summary="创建待办事项",
)
def createtodos(
    todoscreate: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建新的待办事项"""
    new_todo = Todo(
        title=todoscreate.title,
        description=todoscreate.description,
        category=todoscreate.category,
        user_id=current_user.id,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"message": "待办事项创建成功！", "todo": new_todo}


####  GET /todos（列表）
@app.get(
    "/todos",
    status_code=200,
    tags=["待办事项"],
    summary="查看所有待办事项",
)  # 返回列表TodoResponse格式的数组
def GetTodos(
    db: Session = Depends(get_db),
    keyword: str | None = None,  # 搜索标题或描述中包含关键词的
    category: str | None = None,  # 按分类过滤
    completed: bool | None = None,  # 按完成状态过滤
    page: int = 1,  # 页码（从 1 开始）
    size: int = 10,  # 每页10条数据
):
    """获取待办事项列表（支持搜索和分页）"""

    # 1.过滤
    result = db.execute(select(Todo)).scalars().all()
    if keyword:
        result = [t for t in result if keyword.lower() in t.title.lower()]
    if category:
        result = [t for t in result if category.lower() in t.category.lower()]
    if completed is not None:
        result = [t for t in result if t.completed == completed]

    # 2.分页：列表切片
    total = len(result)  # 一共total条数据
    start = (page - 1) * size  # (page - 1)索引从0开始
    end = start + size
    page_data = result[start:end]
    # eg:一页10条数据 取第二页数据：result[10:20]
    # 第二页数据应该从索引10开始 计算方式(2-1)*10=10
    # 结束：10条数据 到索引20结束 计算方式：10+10=20

    return {
        "data": page_data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        },
    }


#### GET /todos/{todo_id}（详情）
@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=200,
    tags=["待办事项"],
    summary="详情",
)
def FindTodos(todo_id: int, db: Session = Depends(get_db)):
    """获取单个待办事项详情"""
    todo = db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")

    return todo


####  PUT /todos/{todo_id}（全量更新）
@app.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=200,
    tags=["待办事项"],
    summary="全量更新",
)
def UpdateTodos(
    todo_id: int,
    todoupdate: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """全量更新待办事项"""
    todo = db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作他人待办")

    todo.title = todoupdate.title
    todo.description = todoupdate.description
    todo.category = todoupdate.category
    todo.completed = todoupdate.completed

    db.commit()

    return todo


####  PATCH /todos/{todo_id}（部分更新）
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["待办事项"],
    summary="部分更新",
)
def PatchTodos(
    todo_id: int,
    todoupdate: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """部分更新待办事项"""
    todo = db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作他人待办")
    update_data = todoupdate.model_dump(
        exclude_unset=True
    )  # model_dump（）把BaseModel 实例对象转为普通 Python 字典 exclude_unset=True获取实际传的字段
    for key, value in update_data.items():
        setattr(todo, key, value)  # 替代update
    db.commit()
    db.refresh(todo)
    return todo


####DELETE /todos/{todo_id}（删除）
@app.delete(
    "/todos/{todo_id}",
    status_code=204,
    tags=["待办事项"],
    summary="删除",
)
def DeleteTodos(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除待办事项"""
    todo = db.get(Todo, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作他人待办")

    db.delete(todo)
    db.commit()
    return None


####GET /todos/stats/summary
@app.get("/todos/stats/summary/{user_id}", tags=["统计"], summary="统计待办事项信息")
def SummaryTodos(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取我的待办事项统计信息"""
    todo = db.execute(select(Todo).where(Todo.user_id == user_id)).scalars().all()

    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    total = len(todo)
    completed = sum(1 for t in todo if t.completed)
    pending = total - completed
    categories = dict(Counter(t.category for t in todo))
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "categories": categories,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
