FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
WORKDIR /app/backend
# 连宿主机 MySQL：容器里的 localhost 是容器自己，要用 host.docker.internal 指回你的电脑
# （生产环境不该把密码写进 Dockerfile，用环境变量/密钥管理，演示先这样）
ENV ASYNC_DATABASE_URL=mysql+aiomysql://root:123456@host.docker.internal:3306/ai_app?charset=utf8mb4
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]