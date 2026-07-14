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

当用户进入此文件夹并开始对话时，请遵循以下规则：

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

当前阶段：第一阶段 | 当前进度：Day 16 已完成 | LeetCode：0题 | 最后更新：2026-07-14

### 练习完成记录
| 日期 | Day | 完成题数 | 掌握度 | 备注 |
|------|-----|---------|--------|------|
| 06-29 | Day1 | 0/5 | 学习中 | 完成课程，练习题已生成未做 |
| 06-29 | Day1-2 | 3/4 | 良好 | homework1-2/3/4正确，homework1-1的f-string和bool()待修复 |
| 06-30 | Day3 | 5/5 | 良好 | 条件判断练习全部完成，homework3-4第15行直角三角形判断有笔误，homework3-5缺少双错情况 |
| 06-30 | Day1-3 总复习 | 全部完成 | 良好 | Day1-3所有练习已完成，之前的问题（homework1-1的f-string/bool()、homework3-4直角判断、homework3-5双错情况）均已修复 |
| 07-01 | Day4 | 5/5 | 良好 | 循环练习全部完成，homework4-2变量名错误已修复，homework4-5素数逻辑错误已修复 |
| 07-02 | Day5 | 5/5 | 良好 | 列表/元组/字典/集合练习全部完成，homework5-2索引赋值→append修复，homework5-5用split+循环/推导式处理输入 |
| 07-05 | Day8 | 4/4 | 良好 | 函数定义/参数/返回值练习完成（greet/add/is_even/max_of_three/咖啡订单/*args/**kwargs/analyze_numbers） |
| 07-05 | Day7 | 5/5 | 良好 | FizzBuzz/回文判断/数字反转/石头剪刀布/学生成绩管理系统全部完成，homework7-4输入合法性检查无效（else永远不会执行，需提前拦截非法输入） |
| 07-06 | Day9 | 3/3 | 良好 | 作用域(global)/lambda(sorted+key)/map+filter练习完成，homework9-2按成绩排序(sorted+key=lambda x:x[1])已掌握，homework9-3的filter用x if..else''而非布尔值（功能对但不规范，建议改x>0） |
| 07-07 | Day10 | 3/3 | 良好 | 异常处理练习全部完成。homework10-1：原版无return导致print输出None，已修复为return结果/错误信息，并将except ValueError改为TypeError接住字符串除法(10/'a')。homework10-2：自定义异常AgeError(Exception)+if/raise AgeError+except AgeError as e+else正常分支，三类输入(非数字/超范围/合法)均正确。homework10-3：try/except/finally，原版finally里f未定义致UnboundLocalError(且调用传整数1/2致OSError而非FileNotFoundError)，已修复为f=None初始化+if f:兜底close，调用改传文件名字符串。注意：homework10-2的❌/✅emoji在GBK控制台会UnicodeEncodeError（环境问题非逻辑错） |
| 07-09 | Day11 | 3/3 | 良好 | 文件操作练习全部完成。homework11-1：txt读写，原版反复open无close，已改用with语句按用途分开(r/w/a)。homework11-2：CSV读写，原版writelines写嵌套列表失败+readlines遍历到字符级，已改用csv.writer/reader；最高平均分用循环内跟踪max_avg+best_name实现。homework11-3：JSON读写，功能正确，有小瑕疵(dumped变量无用/row['done']==True冗余) |
| 07-10 | Day12 | 2/2 | 良好 | 模块与包练习全部完成。模块基础：__all__控制import *、import/as别名导入。homework12-1：自定义math模块(add/subtract/multiply/divide)+main文件import as调用。homework12-2：第三方库requests获取API数据，注意到SSL证书过期问题并用verify=False绕过(正确做法) |
| 07-10 | Day13 | 4/4 | 良好 | 标准库练习全部完成。homework13-1：datetime(今天日期/距生日天数/已出生天数)用strftime格式化+timedelta计算。homework13-2：random生成10个随机数+shuffle原地打乱列表。homework13-3：collections.Counter(abracadabra).most_common(2)+defaultdict(list)按科目分组统计成绩。homework13-4：re正则表达式提取邮箱/电话号码+手机号验证(1[3-9]\d{9}) |
| 07-11 | Day14 | 1/1 | 良好 | 综合项目——命令行记账本完成。6大功能：记一笔(自增ID/日期默认今天)、查看所有(格式化输出)、按类别筛选(.strip()兼容空格)、删除记录(按ID+异常处理)、统计汇总(收入/支出按类别细分)、退出保存(JSON持久化+启动自动加载)。全功能try/except异常处理覆盖 |
| 07-12 | Day15 | 2/2 | 良好 | 面向对象基础——类与对象。day15-1：Turtle类理解__init__构造方法、实例属性vs类属性、self的含义。homework15-1：Student类（__init__默认参数None避免可变陷阱、add_score/append、average/ZeroDivisionError、introduce调用方法加()）。homework15-2：BankAccount类（私有属性_balance约定、deposit/withdraw/get_balance封装） |
| 07-14 | Day16 | 2/2 | 良好 | 继承、多态、装饰器。homework16-1：Animal/Dog/Cat继承体系（super().__init__传递name、speak方法签名一致性、f-string格式化、多态函数make_sound）。homework16-2：BankAccount封装（_balance私有属性、deposit/withdraw余额操作、@property改造get_balance为属性访问） |

### 项目完成情况
| 阶段 | 项目 | 状态 | 备注 |
|------|------|------|------|
| 第一阶段 Week2 | 命令行记账本 | ✅ 已完成 | 2026-07-11 完成，含JSON持久化+异常处理 |
| 第一阶段 Week3 | 面向对象重构记账本 | 未开始 | |
