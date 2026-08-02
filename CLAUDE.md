# AI 应用开发学习项目

## 用户背景

- 软件工程，准大四学生（民办三本）
- 编程基础薄弱：会基本语法和环境配置，但生疏，无法独立完成项目
- 目标：2026 年 12 月左右找到 AI 应用开发方向的实习
- 每天学习时间：暑假 6-8 小时，开学后 4-5 小时
- 英语：借助翻译工具可以阅读英文文档
- 电脑配置：有 NVIDIA 显卡，可以本地跑模型

## 学习路线文档

本文件夹下有一份完整的学习路线文档：`AI应用开发学习路线.docx`

该文档涵盖 7 个阶段、168 天的详细学习计划（2026年7月 - 12月底）：

| 阶段 | 时间 | 内容 |
|------|------|------|
| 第一阶段 | Week 1-3（7.1-7.21） | Python 基础夯实 |
| 第二阶段 | Week 4-6（7.22-8.11） | Web 开发基础（FastAPI + 数据库） |
| 第三阶段 | Week 7-8（8.12-8.25） | LLM API 入门 + 第一个 AI 项目 |
| 第四阶段 | Week 9-11（8.26-9.15） | RAG 系统开发（简历项目一） |
| 第五阶段 | Week 12-15（9.16-10.13） | AI Agent 开发（简历项目二） |
| 第六阶段 | Week 16-18（10.14-11.3） | 计算机基础突击 + 项目打磨 |
| 第七阶段 | Week 19-24（11.4-12月底） | 求职冲刺 |

## 交互规则

当用户进入此文件夹并开始对话时，请遵循以下 rules：

### 1. 识别学习状态
- **先读下方「学习进度」区块**，直接获取用户当前阶段、Day、已完成题数
- 如果进度区块显示用户很久没更新，主动询问是否有新进展
- 根据进度提供对应阶段的帮助

### 2. 教学原则
- **引导优先于直接给答案**：用户在学习阶段，需要理解原理而不是只要代码
- **解释要通俗易懂**：用户基础薄弱，避免用太多专业术语，用类比和生活化例子
- **代码要有详细注释**：每一行代码都要解释它在做什么
- **主动检查理解**：教完一个知识点后，可以出一个小练习让用户巩固
- **中文回答为主**：用户英语需要借助翻译工具，技术术语保留英文但给出中文解释

### 3. 帮助范围
- 解答当前学习阶段的知识点疑问
- 帮助 debug 用户写的项目代码
- 解释教程中看不懂的概念
- 指导 LeetCode 刷题（给思路而不是直接给答案）
- 项目遇到困难时提供方向性指导
- 面试准备阶段的模拟面试和技术问答

### 4. 进度追踪
- 用户说"做完了 Day X 练习"、"更新进度"、"看看进度"时，执行以下流程：
  1. 扫描对应文件夹的 .py 文件，检查完成情况
  2. 更新下方「学习进度」表格
  3. **自动提交代码到 GitHub**：`git add .` → `git commit` → `git push`
- 如果发现用户在某个难点卡住太久（超过 2 天），建议调整策略
- 定期提醒用户写笔记、刷 LeetCode

### 5. 技术栈（按学习顺序）
Python → FastAPI → Streamlit → SQLite/SQLAlchemy → LLM API（通义千问/OpenAI/GLM）→ Ollama → ChromaDB → LangChain → LangGraph → Docker → Git

## 重要提醒

- 用户时间紧迫，不要建议"再多学几个月基础"
- 用户目标明确是 AI **应用**开发，不是 AI 算法/模型研究
- 鼓励为主，但不要降低技术要求的标准
- 如果用户想跳过某个阶段，先确认他理解跳过的风险

## 学习进度

当前阶段：第二阶段 | 当前进度：Day 35 已完成 | LeetCode：0题 | 最后更新：2026-08-02

### 练习完成记录
| 日期 | Day | 完成题数 | 掌握度 | 备注 |
|------|-----|---------|--------|------|
| 08-02 | Day35 | 综合项目 | 良好 | 综合项目：Todo API 用户系统。给 Day28 的待办 API 加上完整用户系统：新增 User 表+Todo 关联 user_id(每个待办属于一个用户)。核心功能：POST /auth/register 注册/bcrypt密码哈希(passlib CryptContext schemes=["bcrypt"])/POST /auth/login 登录+JWT签发(HS256+ACCESS_TOKEN_EXPIRE_MINUTES=30)/OAuth2PasswordBearer+get_current_user鉴权依赖/全部操作需带Token/权限控制(只能改删自己的待办)/CORS中间件(ALLOWED_ORIGINS从.env读)/环境变量(DATABASE_URL/SECRET_KEY/DEBUG)。14个路由：/auth/register+login、/todos/me(我的待办)、/todos CRUD、/todos/stats/summary/{user_id}统计。测试数据insert_test_data.py插入2用户(test 8条+xjx 6条=12条)。验证：venv导入成功，数据库users表2个用户+todos表12条。备注：解决Day33遗留问题——密码哈希用passlib实现了 |
| 08-02 | Day34 | 4/4 | 良好 | 中间件+错误处理+环境变量：4个实验全部完成(CORS中间件/自定义日志中间件+性能监控BaseHTTPMiddleware/环境变量加载python-dotenv+配置/统一错误响应格式RequestValidationError全局异常处理)。掌握：中间件执行流程(Request→Middleware→路由→Response→Middleware)、add_middleware注册顺序后加先执行、CORS跨域原理(同源协议域名端口)、Access-Control-Allow-Origin响应头、严格vs宽松CORS配置(宽松domain+allow_credentials=True会报错)、日志中间件dispatch(call_next)记录耗时、认证中间件白名单绕过、全局异常处理器(validates错误422/HTTPException 4xx/未捕获异常500)统一响应格式(前端只检查res.success===false)、环境变量管理(为什么要用.env/.gitignore、python-dotenv加载、os.getenv默认值、DEBUG字符串转bool、多环境配置.env.development/.env.production)。16个路由验证通过。学习笔记.md系统整理六大部分 |
| 07-31 | Day33 | 5/5 | 良好 | JWT认证基础：5个实验全部完成（创建JWT令牌/jwt.encode()密钥算法/令牌验证依赖/oauth2_scheme/OAuth2PasswordRequestForm登录接口/令牌过期时间设置/Postman测试认证）。掌握：JWT结构(header.payload.signature)/HS256算法安全限制/Depends(get_current_user)权限验证依赖项/TokenData模型验证/401未授权响应。注意：login.py中需处理密码哈希（但本实验简化未实现），实际应使用passlib.hash.bcrypt；main.py的/token路由应返回access_token而非token_type（实验要求简化） |
| 07-29 | Day32 | 5/5 | 良好 | FastAPI+SQLAlchemy集成：5个实验全部完成(依赖注入get_db+Yield/CRUD四接口POST201+GET+PUT全量更新+PATCH部分更新+DELETE204/搜索过滤+分页+分类统计+聚合查询/事务回滚rollback+flush对比/批量插入性能对比)。掌握Depends()依赖注入原理(yield+finally保证清理)/Session生命周期管理/PUT(全量替换)vsPATCH(部分更新exclude_unset=True)/func.count数据库聚合vslen内存统计/事务ACID特性(commit持久化vsflush暂存)/批量操作优化(add_all+一次commit比逐条commit快221倍)。注意：main.py中Todo模型缺少category字段导致分类统计无法测试，需补充字段或换表测试 |
| 07-28 | Day31 | 5/5 | 良好 | Alembic迁移+数据库设计：5个实验全部完成(alembic init初始化+autogenerate自动生成迁移+upgrade执行迁移/downgrade回滚/范式判断1NF-2NF-3NF/索引性能对比)。掌握Alembic完整流程(init→revision --autogenerate→upgrade head)/env.py配置(target_metadata+sys.path)/migration chain迁移链(base→001→002→head)/downgrade -1回退一步vs downgrade base全部回滚/autogenerate局限性(不能改列名改列类型需手动)/SQLite重建表机制。三大范式：1NF原子性/2NF无部分依赖(复合主键)/3NF无传递依赖。索引：B+树/最左前缀原则/EXPLAIN QUERY PLAN看执行计划(SCAN全表vs SEARCH索引)。修正：4-B答案从2NF改为3NF(单列主键无部分依赖，customer_name通过customer_id传递依赖主键=违反3NF非2NF)/4-C的3NF答案确认正确/3.1细化分情况(DROP COLUMN只丢该列数据vs DROP TABLE全没)/2.2补充SQLite重建表机制(临时表→拷贝→删旧→重命名) |
| 07-28 | Day30 | 5/5 | 良好 | SQLAlchemy ORM基础：5个实验全部完成(模型定义User+Todo一对多关系/Session CRUD增删改查/过滤排序分页joinedload关联查询/外键约束级联删除)。掌握了ORM概念(Python对象代替SQL)/DeclarativeBase建模型/ForeignKey+relationship实现一对多/back_populates双向关联/cascade级联操作/sessionmaker会话管理/add/commit/query/filter/all/delete/diff(flush不提交vs commit持久化)/joinedload解决N+1问题。修正：3.2题desc/asc含义写反了(desc降序非升序)、1.1 cascade解释需补充delete-orphan孤儿、1.2 back_populates两边声明解释优化 |
| 07-27 | Day29 | 5/5 | 良好 | SQL基础+SQLite：5个实验全部完成(建表INSERT/SELECT查询UPDATE DELETE/JOIN多表/聚合函数GROUP BY HAVING)。掌握了CRUD操作、防SQL注入(?占位符)、LIKE模糊匹配、分页(LIMIT/OFFSET)、INNER JOIN vs LEFT JOIN区别、聚合函数COUNT/SUM/AVG/MAX/MIN、sqlite3命令行+Python sqlite3模块。需注意：4.1题INNER/LEFT JOIN解释写反了、2.4分页测试建议跑main.py验证参考答案差异、2.1 LIMIT-OFFSET顺序描述需精简为标准写法 |
| 07-26 | Day28 | 5/5 | 良好 | 综合项目：待办事项API。Step1(FastAPI初始化+内存存储+健康检查)/Step2(CRUD五接口：POST创建201+GET列表+GET详情404+PUT全量更新+DELETE删除204)/Step3(搜索过滤keyword/category/completed+列表切片分页+PATCH部分更新exclude_unset)/Step4(JSON文件持久化load_todos/save_todos)/Step5(Counter统计categories+tags/summary文档)。修复Bug：date.today()转str用.isoformat()/completed过滤bool无.lower()/total.size→total/size除法/response_model与分页字典冲突删List[TodoResponse]/PATCH的todo_id漏写int类型注解/stats路由被{todo_id}拦截需移到前面/load_todos()的return[]缩进错误导致首次运行返回None |
| 07-24 | Day27 | 6/6 | 良好 | FastAPI进阶：请求体Pydantic BaseModel(BookCreate)/Field验证规则(min_length/gt/le/ge+破坏性实验default=0不满足gt=0)/响应模型response_model过滤password字段/嵌套模型Address+CompanyCreate+列表字段/HTTPException 404错误处理+DELETE 204/混合参数(路径参数+查询参数+请求体)+exclude_unset=True。额外完成apps子项目：app03(Pydantic field_validator自定义验证+Addr嵌套+List类型)、app04(Form表单数据接收)。修复：main.py的price Field破坏性实验default=0未改回...(已修复)、GET路由/todo少写s(已修复)。注意：homework27问题2.1的gt/ge含义写反了(gt=大于不是小于)，需记住gt=greater than/ge=greater than or equal |
| 07-23 | Day26 | 7/7 | 良好 | FastAPI入门7个实验全部完成：Hello World基础API/路径参数int类型验证+422错误观察/查询参数默认值+Optional/路径+查询混合参数/Enum枚举限制选项(asc/desc)/自定义状态码201+204/自动文档Swagger UI配置(title/description/tags/docstring)。额外完成：原始socket HTTP服务器(day26-http.py)、4种HTTP方法装饰器(@get/@post/@put/@delete)、路由分发模式(主app+子router)、请求响应子项目(路径参数优先级+Union/Optional查询参数)。遗留小问题：main.py里POST /users路由重复(实验6和7冲突)、user_id类型破坏性实验后未改回int、请求和响应/子项目缺__init__.py |
| 07-22 | Day25 | 5/5 | 良好 | 异步编程基础：执行顺序预测(gather并发按完成时间排序)/同步vs异步耗时对比(sync 3.0s→async 1.0s,3倍提升)/异步爬虫模拟(5网站并发5.8s→2.0s,节省3.8s)/async常见错误找茬(3个:未await协程/普通函数用await/async里用time.sleep)/异步倒计时器(while循环+asyncio.sleep双并发)。核心修复：exercise_2加async def+调用处await+内部asyncio.run改await(不能嵌套事件循环)。掌握核心规则：一个程序只有一个asyncio.run()入口，内部用await |
| 07-21 | Day24 | 5/5 | 良好 | RESTful API设计：在线书店API CRUD设计(10题)/社交媒体API找茬修正(6题)/JSON序列化反序列化+文件读写(3题)/统一响应格式3函数(成功/错误/分页列表)/HTTP状态码选择(8题：201/406/413/429/503/304/204/301)。掌握了RESTful核心原则（URL=名词/方法=动词、复数名词、嵌套≤2层、查询参数过滤分页），理解了PUT(全量)vs PATCH(部分)、201vs204、304缓存机制 |
| 07-21 | Day23 | 5/5 | 良好 | 观察HTTP请求：F12观察B站搜索API/请求头/Cookie+自建HTTP服务器(GET/POST+修复404双重send_response bug)+requests实验(UA伪装/Session管理Cookie/超时控制)+curl 5命令+Postman/Apifox 4任务。额外完成本地httpbin项目(my_httpbin.py)，支持6个端点(/get、/post、/status、/headers、/delay、/)，作为后续Day24-28的长期调试工具 |
| 07-19 | Day22 | 9/9 | 良好 | HTTP协议基础：URL结构/HTTP方法/状态码/请求头/requests库GET-POST/CRUD模拟。遇到httpbin.org连接问题，改用postman-echo.com完成。深入理解了GET vs POST区别（params vs json）、405状态码、请求头回显原理、301重定向机制 |
| 07-16 | Day19 | 2/2 | 良好 | 类型注解/dataclass/Enum/Pydantic笔记+homework19-1/2完成 |
| 07-17 | Day20 | 1/1 | 良好 | 综合项目：用面向对象重构记账本完成。Record类+AccountBook类(add/delete/search/update/get_all/get_by_id/summary)+JSON持久化+命令行主菜单 |

| 06-29 | Day1 | 0/5 | 学习中 | 完成课程，练习题已生成未做 |
| 06-29 | Day1-2 | 3/4 | 良好 | homework1-2/3/4正确，homework1-1的f-string和bool()待修复 |
| 06-30 | Day3 | 5/5 | 良好 | 条件判断练习全部完成，homework3-4第15行直角三角形判断有笔误，homework3-5缺少双错情况 |
| 06-30 | Day1-3 总复习 | 全部完成 | 良好 | Day1-3所有练习已完成，之前的问题（homework1-1的f-string/bool()、homework3-4直角判断、homework3-5双错情况）均已修复 |
| 07-01 | Day4 | 5/5 | 良好 | 循环练习全部完成，homework4-2变量名错误已修复，homework4-5素数逻辑错误已修复 |
| 07-02 | Day5 | 5/5 | 良好 | 条件判断/循环/列表/元组/字典/集合练习全部完成，homework5-2索引赋值→append修复，homework5-5用split+循环/推导式处理输入 |
| 07-05 | Day8 | 4/4 | 良好 | 函数定义/参数/返回值练习完成（greet/add/is_even/max_of_three/咖啡订单/*args/**kwargs/analyze_numbers） |
| 07-05 | Day7 | 5/5 | 良好 | FizzBuzz/回文判断/数字反转/石头剪刀布/学生成绩管理系统全部完成，homework7-4输入合法性检查无效（else永远不会执行，需提前拦截非法输入） |
| 07-06 | Day9 | 3/3 | 良好 | 作用域(global)/lambda(sorted+key)/map+filter练习完成，homework9-2按成绩排序(sorted+key=lambda x:x[1])已掌握，homework9-3的filter用x if..else''而非布尔值（功能对但不规范，建议改x>0） |
| 07-07 | Day10 | 3/3 | 良好 | 异常处理练习全部完成。homework10-1：原版无return导致print输出None，已修复为return结果/错误信息，并将except ValueError改为TypeError接住字符串除法(10/'a')。homework10-2：自定义异常AgeError(Exception)+if/raise AgeError+except AgeError as e+else正常分支，三类输入(非数字/超范围/合法)均正确。homework10-3：try/except/finally，原版finally里f未定义致UnboundLocalError(且调用传整数1/2致OSError而非FileNotFoundError)，已修复为f=None初始化+if f:兜底close，调用改传文件名字符串。注意：homework10-2的❌/✅emoji在GBK控制台会UnicodeEncodeError（环境问题非逻辑错） |
| 07-09 | Day11 | 3/3 | 良好 | 文件操作练习全部完成。homework11-1：txt读写，原版反复open无close，已改用with语句按用途分开(r/w/a)。homework11-2：CSV读写，原版writelines写嵌套列表失败+readlines遍历到字符级，已改用csv.writer/reader；最高平均分用循环内跟踪max_avg+best_name实现。homework11-3：JSON读写，功能正确，有小瑕疵(dumped变量无用/row['done']==True冗余) |
| 07-10 | Day12 | 2/2 | 良好 | 模块与包练习全部完成。模块基础：__all__控制import *、import/as别名导入。homework12-1：自定义math模块(add/subtract/multiply/divide)+main文件import as调用。homework12-2：第三方库requests获取API数据，注意到SSL证书过期问题并用verify=False绕过(正确做法) |
| 07-10 | Day13 | 4/4 | 良好 | 标准库练习全部完成。homework13-1：datetime(今天日期/距生日天数/已出生天数)用strftime格式化+timedelta计算。homework13-2：random生成10个随机数+shuffle原地打乱列表。homework13-3：collections.Counter(abracadabra).most_common(2)+defaultdict(list)按科目分组统计成绩。homework13-4：re正则表达式提取邮箱/电话号码+手机号验证(1[3-9]\d{9}) |
| 07-11 | Day14 | 1/1 | 良好 | 综合项目——命令行记账本完成。6大功能：记一笔(自增ID/日期默认今天)、查看所有(格式化输出)、按类别筛选(.strip()兼容空格)、删除记录(按ID+异常处理)、统计汇总(收入/支出按类别细分)、退出保存(JSON持久化+启动自动加载)。全功能try/except异常处理覆盖 |
| 07-12 | Day15 | 2/2 | 良好 | 面向对象基础——类与对象。day15-1：Turtle类理解__init__构造方法、实例属性vs类属性、self的含义。homework15-1：Student类（__init__默认参数None避免可变陷阱、add_score/append、average/ZeroDivisionError、introduce调用方法加()）。homework15-2：BankAccount类（私有属性_balance约定、deposit/withdraw/get_balance封装） |
| 07-15 | Day18 | 2/2 | 良好 | 装饰器timer(闭包+*args/**kwargs通用转发/f-string格式注意)；homework18-2初稿问题：原函数未调用(timer()而非func)、时间算反、返回值错误、f-string空格报错 |
| 07-15 | Day17 | 1/1 | 良好 | 魔法方法(__str__/__repr__/__len__/__eq__/__lt__/__call__/__getitem__/__iter__+__next__/__enter__+__exit__)，笔记三份+homework17-1完成 |

### 项目完成情况
| 阶段 | 项目 | 状态 | 备注 |
|------|------|------|------|
| 第一阶段 Week2 | 命令行记账本 | ✅ 已完成 | 2026-07-11 完成，含JSON持久化+异常处理 |
| 第一阶段 Week3 | 面向对象重构记账本 | ✅ 已完成 | 2026-07-17 完成，含Record/AccountBook类设计、JSON持久化、命令行交互 |
| 第二阶段 Week4 | 待办事项API | ✅ 已完成 | 2026-07-26 完成，含CRUD+搜索分页+PATCH部分更新+JSON持久化+Counter统计
| 第二阶段 Week5 | Todo API 用户系统 | ✅ 已完成 | 2026-08-02 完成，含User表+注册/登录+bcrypt密码哈希+JWT认证+OAuth2鉴权+权限控制+CORS+环境变量