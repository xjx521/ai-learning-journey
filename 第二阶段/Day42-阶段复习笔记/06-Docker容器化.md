# 🐳 第二阶段学习笔记(六):Docker 容器化

> 📅 学习周期:2026.08.12 | 对应 Day41
> 📌 作用:把 Day39-40 的 FastAPI 应用容器化,让它"随处都能跑"。Docker 是**部署/环境管理**的必备技能,后续阶段和实习都要用
> 🎯 掌握后应能:看懂 Dockerfile、构建镜像、启动容器、用 docker-compose 一键启动多服务

---

## 目录

- [第 18 章 Docker 基础](#-第-18-章-docker-基础)
  - [18.1 镜像 vs 容器](#181-镜像-vs-容器)
  - [18.2 Docker vs 虚拟机](#182-docker-vs-虚拟机)
  - [18.3 Dockerfile 核心指令](#183-dockerfile-核心指令)
  - [18.4 核心命令](#184-核心命令)
  - [18.5 端口映射](#185-端口映射)
  - [18.6 docker-compose](#186-docker-compose)
  - [18.7 容器连宿主机数据库](#187-容器连宿主机数据库)
- [🎯 第 18 章 面试/开发高频考点](#-第-18-章-面试开发高频考点)
- [📕 本册错题本](#-本册错题本)

---

# 第 18 章 Docker 基础

## 18.1 镜像 vs 容器

### 🔴 模板(镜像) vs 实例(容器)

> 📌 **知识点说明**:**镜像(Image) = 只读模板/安装包,容器(Container) = 镜像跑起来的实例,可以启动/停止/删除**。一个镜像能同时跑出多个互不影响的容器。
>
> 类比:模具和披萨 —— 镜像是一套模具,容器是模具做出来的披萨;模具做多少次都能用,每张披萨是独立的个体。

| 对比 | 镜像 Image | 容器 Container |
|------|-----------|---------------|
| 本质 | 只读模板(代码+依赖+配置) | 镜像运行的实例(可读写) |
| 类比 | 模具 / 安装包 | 模具做出的披萨 / 运行中的程序 |
| 能改吗 | 不能直接改(要重新 build) | 可以(有自己的一层) |
| 数量 | 一套镜像 | 一个镜像可跑多个容器 |
| 删除 | 删除镜像不影响在跑的容器 | 删除容器不影响镜像 |

💡 **速记**:`docker build` 做出镜像,`docker run` 把镜像变成容器。

## 18.2 Docker vs 虚拟机

### 🔴 只装应用 vs 装整套系统

> 📌 **知识点说明**:虚拟机(VM)模拟**整套操作系统**(重、启动慢、占资源);Docker 容器只装**应用 + 依赖**,共享宿主机的操作系统内核(**轻、启动秒级**)。

| 对比 | Docker 容器 | 虚拟机 VM |
|------|-----------|-----------|
| 包含 | 只装应用 + 依赖 | 完整操作系统 |
| 大小 | MB 级 | GB 级 |
| 启动 | 秒级 | 分钟级 |
| 资源占用 | 低(共享内核) | 高(每台都装系统) |
| 隔离 | 进程级隔离 | 完整隔离 |

## 18.3 Dockerfile 核心指令

### 🔴 构建镜像的"配方单"(面试必背套路)

> 📌 **知识点说明**:Dockerfile 是一步一步描述"怎么把项目打包成镜像"的文本。**标准套路顺序固定:FROM → WORKDIR → COPY requirements → RUN install → COPY 代码 → EXPOSE → CMD**,每一行都生成镜像的一层。

```dockerfile
# 1. 基础镜像:从哪开始(官方 Python 精简版)
FROM python:3.14.6-slim

# 2. 工作目录:后面所有命令都在这个目录里执行
WORKDIR /app

# 3. 先拷贝依赖清单(单独拷,利用缓存,改代码不用重装依赖)
COPY requirements.txt .

# 4. 安装依赖(在容器里装)
RUN pip install -r requirements.txt --no-cache-dir

# 5. 再拷贝项目代码(代码改动频繁,放后面 = 构建更快)
COPY . .

# 6. 声明端口(注意:只是"说明书",不真正开端口)
EXPOSE 8000

# 7. 容器启动时执行的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| 指令 | 作用 | 易错点 |
|------|------|--------|
| FROM | 指定基础镜像 | 必须第一行 |
| WORKDIR | 设置工作目录 | 相当于 cd |
| COPY | 从本机拷文件进容器 | 目标相对 WORKDIR |
| RUN | 构建时执行命令(装依赖) | 在构建阶段运行 |
| EXPOSE | **声明**端口(文档) | ⚠️ 不真的开端口 |
| CMD | 容器启动时执行的命令 | 启动时运行,不是构建时 |

⚠️ **易错点(EXPOSE 只是声明)**:
```bash
# EXPOSE 8000 只写进"说明书",真正把端口暴露给宿主机要靠 docker run -p
# ❌ docker run 镜像名        # 容器内 8000 外面访问不到!
# ✅ docker run -p 8000:8000 镜像名   # 左=本机端口,右=容器端口
```

## 18.4 核心命令

### 🔴 build / run / ps / logs / stop(必会)

> 📌 **知识点说明**:构建镜像和运行容器是 Docker 日常最高频的命令,其余是"查看、看日志、停止"三件套。

```bash
# 构建镜像:-t 给镜像起名字,最后的 . 是 Dockerfile 所在目录
docker build -t my-fastapi-app .

# 运行容器:-p 端口映射,-d 后台运行,--name 给容器起名字
docker run -p 8000:8000 -d --name my-app my-fastapi-app

# 查看运行的容器(-a 连已停止的一起看)
docker ps
docker ps -a

# 看日志(调试必备)
docker logs my-app

# 停止容器
docker stop my-app

# 删除容器 / 镜像
docker rm my-app
docker rmi my-fastapi-app
```

| 命令 | 作用 | 常用选项 |
|------|------|---------|
| `docker build -t 名字 .` | 构建镜像 | -t 名字 |
| `docker run -p 8000:8000 镜像` | 运行容器 | -p 映射 / -d 后台 / --name |
| `docker ps` | 查看运行中容器 | -a 全看 |
| `docker logs 容器` | 看容器日志 | -f 跟随 |
| `docker stop 容器` | 停止容器 | |
| `docker rm` / `docker rmi` | 删容器 / 删镜像 | -f 强制 |

## 18.5 端口映射

### 🔴 -p 左边本机,右边容器

> 📌 **知识点说明**:容器是独立"盒子",外面的电脑访问不到容器内部的服务,必须用 `-p` 把容器的端口"接出来"。**格式:`-p 本机端口:容器端口`。右是容器里 uvicorn 监听的口,左是你浏览器访问的口**。

```bash
# 容器里 uvicorn 监听 8000,本机 8000 → 容器 8000
docker run -p 8000:8000 my-fastapi-app
# 浏览器访问 http://localhost:8000

# 也可以换本机端口(改成 9000):访问 http://localhost:9000
docker run -p 9000:8000 my-fastapi-app
```

⚠️ **易错点:--host 0.0.0.0 必须写**:
```python
# ❌ uvicorn main:app --host 127.0.0.1   # 只允许容器内部访问,外面连不上!
# ✅ 必须监听 0.0.0.0,才允许从容器外(宿主机)访问
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
> 📌 理解:`127.0.0.1` = 只允许本机自己访问(容器里指容器自己),`0.0.0.0` = 允许任何来源访问。

## 18.6 docker-compose

### 🟡 一键启动多个服务

> 📌 **知识点说明**:一个项目往往要"后端 + 数据库 + 前端"多个容器,`docker-compose.yml` 用**一个文件声明所有服务**,一条命令全部启动。**核心结构:每个缩进两层缩进的 key 是一个服务**,可写 `build`(用 Dockerfile 构建)或 `image`(用现成镜像)。

```yaml
version: "3.8"

services:                      # 顶层:services
  backend:                     # 服务1:后端(两层缩进 = 一个服务)
    build: .                   # 用当前目录的 Dockerfile 构建
    ports:                     # 端口映射
      - "8000:8000"
    environment:               # 环境变量(相当于 .env 注入)
      - DATABASE_URL=mysql+pymysql://root:123456@host.docker.internal:3306/ai_app
    depends_on:                # 依赖:先启动 db 再启动 backend
      - db

  db:                          # 服务2:数据库(用现成镜像)
    image: mysql:8.0           # 直接拉官方 MySQL 镜像
    environment:
      MYSQL_ROOT_PASSWORD: "123456"
      MYSQL_DATABASE: ai_app
    volumes:                   # 数据卷:数据库数据存宿主机,容器删了不丢
      - mysql-data:/var/lib/mysql

volumes:                       # 声明命名数据卷
  mysql-data:
```

```bash
docker-compose up -d     # 启动所有服务(-d 后台)
docker-compose down      # 停止并删除所有服务
docker-compose ps        # 查看服务状态
docker-compose logs      # 查看所有服务日志
```

| 字段 | 作用 |
|------|------|
| build | 用本地 Dockerfile 构建 |
| image | 用现成镜像(如 mysql:8.0) |
| ports | 端口映射 `本机:容器` |
| environment | 注入环境变量 |
| volumes | 数据持久化(容器删了数据不丢) |
| depends_on | 服务启动顺序(先启动数据库) |

## 18.7 容器连宿主机数据库

### 🟡 host.docker.internal

> 📌 **知识点说明**:容器里访问宿主机(你的电脑)的服务,**不能写 localhost** —— 容器里的 localhost 是容器自己!要连你电脑上装的 MySQL,用特殊域名 **`host.docker.internal`** 指回宿主机。

```python
# ❌ 容器里连不上!localhost 是容器自己,里面没装 MySQL
# DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/ai_app"

# ✅ 用 host.docker.internal 指回宿主机(你的电脑)
DATABASE_URL = "mysql+aiomysql://root:123456@host.docker.internal:3306/ai_app"
```

> 📌 类比:你在宿舍(容器)里打电话回家(宿主机的 MySQL),不能拨"宿舍本地分机"(localhost),要拨"跨宿舍的总机"(host.docker.internal)。

---

## 🎯 第 18 章 面试/开发高频考点

**必问**:
1. 镜像和容器的区别?(模板 vs 实例,类比模具/披萨)
2. Dockerfile 的套路顺序?(FROM→WORKDIR→COPY requirements→RUN→COPY代码→EXPOSE→CMD)
3. EXPOSE 和 -p 的区别?(EXPOSE 只声明,-p 真正映射端口)
4. 为什么 CMD 里要 --host 0.0.0.0?(否则容器外访问不到)
5. docker build / run / ps / logs / stop 各干嘛?

**加分项**:
- docker-compose 用一条命令启动多服务(services 结构)
- 知道容器连宿主机用 host.docker.internal
- 知道 volumes 数据卷(容器删了数据不丢)

**冷门**:
- Docker 容器共享宿主机内核,比 VM 轻
- COPY 分两次拷(先依赖后代码)利用缓存加速构建

---

# 📕 本册错题本

| # | 错误代码/场景 | 报错/现象 | 原因 | 修复 |
|---|--------------|----------|------|------|
| 1 | requirements.txt 误写"docker练习" | docker build 时 pip install 失败 | 文件里混了非依赖文字 | 改成真实依赖 fastapi/uvicorn/sqlalchemy/aiomysql |
| 2 | 只 EXPOSE 不 -p | 外面访问不到 | EXPOSE 只是声明 | `docker run -p 8000:8000` |
| 3 | CMD 用 --host 127.0.0.1 | 容器外连不上 | 只监听容器内部 | `--host 0.0.0.0` |
| 4 | 容器里连 localhost MySQL | 连接被拒 | 容器的 localhost 是容器自己 | `host.docker.internal` |
| 5 | `docker run 镜像名` 忘端口映射 | 访问 localhost:8000 失败 | 端口没接出来 | 加 `-p 8000:8000` |
