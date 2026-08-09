# Day 41 练习题：Docker 基础

> ⚠️ 前置准备：安装 Docker Desktop（Windows 版），并启动。
> 验证是否装好：在终端跑 `docker --version`，能显示版本号即可。
>
> 🛠 关于「留白」：下面题目里关键命令/指令留空成 `____`，每题开头有 💡 提示。
> 先自己填，再翻到【文件最底部】的参考答案。答案隔开了大量空行，不容易看到。

---

## 【实验 1】概念：镜像 vs 容器

**目标**：理解 Docker 两大核心概念

📝 **问题 1.1**：镜像（Image）和容器（Container）的区别是？
- 镜像是一个模板/安装包 是打包好的应用 只读_不能改___（一个模板/安装包，只读）
- 容器是_镜像跑起来的一个实例，可启动/停止/删除___（镜像跑起来的一个实例，可启动/停止/删除）
- 类比：镜像是__做披萨的模具__，容器是__根据模具做出来的披萨__。
  💡 提示：想想"模具"和"做出来的披萨"。

📝 **问题 1.2**：一个镜像能跑出几个容器？
- 答：_很多__个（互不影响）。
  💡 提示：一个模具能做很多披萨。

📝 **问题 1.3**：Docker 和虚拟机（VM）相比，主要优势是？
- 答：Docker 只装__应用+依赖__，更___轻_（轻/重），启动更__快__（快/慢）。
  💡 提示：一个装完整系统，一个只装应用+依赖。

📝 **问题 1.4**：Docker 到底解决了什么痛点？（一句话）
- 答：___________代码在别人的电脑运行正常，在自己电脑跑不起来_____________________________________
  💡 提示：想想"换台电脑跑不起来"的依赖问题。

---

## 【实验 2】写一个 Dockerfile

**目标**：把下面这个 FastAPI 应用容器化，补全 Dockerfile 的关键指令

假设目录下有 `main.py`（FastAPI 应用）和 `requirements.txt`。

📝 **填空 2.1**：补全 Dockerfile

```dockerfile
# 从 python 3.11 基础镜像开始（第一行必须）
_FROM___ python:3.11-slim
# 💡 提示：用 FROM 指令

# 设置工作目录 /app
_WORKDIR___ /app
# 💡 提示：用 WORKDIR

# 把 requirements.txt 复制进容器
__COPY__ requirements.txt .
# 💡 提示：用 COPY

# 安装依赖
__RUN__ pip install -r requirements.txt
# 💡 提示：用 RUN

# 把当前目录所有文件复制进容器
__COPY__ . .
# 💡 提示：用 COPY

# 声明暴露 8000 端口
_EXPOSE___ 8000
# 💡 提示：用 EXPOSE

# 容器启动时执行 uvicorn
__CMD__ ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# 💡 提示：用 CMD
```

📝 **问题 2.2**：`EXPOSE 8000` 和 `docker run -p 8000:8000` 有什么区别？
- `EXPOSE` 只是__声明__（声明/实际映射），真正让外部能访问靠的是_docker run -p 8000:8000___。
  💡 提示：一个只是"说明"，一个才是"实际打通"。

📝 **问题 2.3**：为什么 `CMD` 里要写 `--host 0.0.0.0` 而不是 `127.0.0.1`？
- 答：因为_0.0.0.0___，容器外才能访问。
  💡 提示：127.0.0.1 只允许容器内部自己访问。

---

## 【实验 3】docker build 和 docker run

**目标**：掌握最核心的两个命令（今天重点）

📝 **填空 3.1**：在 Dockerfile 所在目录构建镜像，名字叫 my-app：

```bash
docker _build___ -t my-app .
# 💡 提示：用 build
```

📝 **填空 3.2**：用镜像 my-app 运行容器，把本机 8000 端口映射到容器 8000：

```bash
docker _run___ -p __8000__:_8000___ my-app
# 💡 提示：用 run；左边本机端口，右边容器端口
```

📝 **填空 3.3**：查看正在运行的容器：

```bash
docker _ps___
# 💡 提示：用 ps
```

📝 **问题 3.4**：`-p 8000:8000` 里"左边"和"右边"分别指什么？
- 左边（8000）是_本机___端口，右边（8000）是__容器__端口。
  💡 提示：一个能被浏览器直接访问，一个在容器内部。

📝 **问题 3.5**：想后台运行容器（不占终端），加什么参数？
- 答：加__-d__。
  💡 提示：用一个字母，detached 的意思。

---

## 【实验 4】docker-compose

**目标**：看懂 docker-compose 用 YAML 一键启动多服务

📝 **填空 4.1**：补全 docker-compose.yml，让它用 backend 目录构建一个后端服务，并映射端口 8000

```yaml
version: "3.8"

services:
  _services___:                      # 服务名
    build: ./backend         # 用 backend 目录的 Dockerfile 构建
    _ports___:                    # 端口映射
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
  # 💡 提示：服务名任意写（如 backend）；端口映射用 ports 字段
```

📝 **填空 4.2**：启动所有服务（后台运行）的命令：

```bash
docker-compose _up___ -d
# 💡 提示：用 up
```

📝 **填空 4.3**：停止并移除所有服务：

```bash
docker-compose __down__
# 💡 提示：用 down
```

📝 **问题 4.4**：`services:` 下面每个"服务"可以写哪些常用字段？（至少写 3 个）
- 答：_builds___、_ports___、__environment__。
  💡 提示：build/image、ports、environment、volumes、depends_on 等。

---

## 【实验 5】实战：容器化你的 FastAPI 应用

**目标**：把 Day 39-40 项目（或 Day 37 的 FastAPI 应用）真正容器化

📝 **任务 5.1**：根据你的项目，写一个 Dockerfile。
- 你有 `main.py`（FastAPI）和 `requirements.txt`，把实验 2 的 Dockerfile 填入真实内容。
- 💡 提示：如果后端入口在 `backend/main.py`，那 `CMD` 里的模块路径要写成 `backend.main:app`（或调整）。

📝 **任务 5.2**：执行下面命令，把应用跑起来：

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
# 浏览器访问 localhost:8000/docs
```

- 记录结果：答：________________________________________________

📝 **任务 5.3**：用 `docker ps` 看容器，用 `docker logs` 看日志，用 `docker stop` 停止。
- 记录你用的命令：________________________________________________

---

## 💡 参考答案（完成所有练习后再看！注意这一行下面空了很多行）





（参考答案在下面，先别急着翻）




### 实验 1 参考答案

1.1：镜像是"模板/安装包（只读）"；容器是"镜像跑起来的一个实例（可操作）"。类比：镜像是"模具"，容器是"做出来的披萨"。
1.2：一个镜像能跑出"多个"容器（互不影响）。
1.3：Docker 只装"应用+依赖"，更"轻"，启动更"快"。
1.4：解决"换台电脑/环境跑不起来"的依赖问题——把应用和它的环境一起打包，随处可跑。

### 实验 2 参考答案

2.1：
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
2.2：EXPOSE 只是"声明"（说明用），真正让外部能访问靠的是 `docker run -p` 的端口映射。
2.3：因为 127.0.0.1 只允许容器内部自己访问，写 0.0.0.0 才能让容器外（本机/其他机器）访问。

### 实验 3 参考答案

3.1：`docker build -t my-app .`
3.2：`docker run -p 8000:8000 my-app`
3.3：`docker ps`
3.4：左边是本机端口，右边是容器端口。
3.5：加 `-d`（detached 后台运行）。

### 实验 4 参考答案

4.1：
```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
```
4.2：`docker-compose up -d`
4.3：`docker-compose down`
4.4：build/image、ports、environment、volumes、depends_on 等（任选 3 个）。

### 实验 5 参考答案

5.1：参照实验 2 的 Dockerfile，注意 CMD 里模块路径要匹配你 main.py 的实际位置。
5.2：`docker build -t my-api .` 后 `docker run -p 8000:8000 my-api`，浏览器访问 localhost:8000/docs 能看到 Swagger。
5.3：`docker ps` 看容器、`docker logs <容器名>` 看日志、`docker stop <容器名>` 停止。

---

## 📌 今日 LeetCode 推荐（可选）

- LeetCode 1 - 两数之和（Easy）：哈希表，练"查找"思维。
- 今天 Docker 偏运维，可先专注把 Dockerfile 跑通，LeetCode 可选。

---

## 学习记录

📝 Day 41 学习打卡

完成时间：____年____月____日

我完成了：
[ ] 实验 1：概念（镜像 vs 容器）
[ ] 实验 2：写 Dockerfile
[ ] 实验 3：docker build / run / ps
[ ] 实验 4：docker-compose
[ ] 实验 5：容器化实战

遇到的问题：
_____________________________________________
_____________________________________________

学到的最重要的一点：
_____________________________________________