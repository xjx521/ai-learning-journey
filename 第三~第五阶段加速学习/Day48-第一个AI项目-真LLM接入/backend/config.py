# config.py 读取的管道，业务代码 = 只依赖 config

from dotenv import load_dotenv
import os

load_dotenv()  # 读取项目根目录的 .env 文件

# 数据库连接
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

# CORS 允许的来源（前端地址）
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")

# 其他
APP_NAME = os.getenv("APP_NAME", "AI 应用模板")
DEBUG = os.getenv("DEBUG", "False") == "True"  # 字符串转布尔
