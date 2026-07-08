#### 题目 2：CSV 文件操作 ⭐⭐⭐

import csv
students=[
    ["姓名","语文","数学","英语"],
    ["小明","85","92","78"],
    ["小红","90","88","95"],
    ["小刚","72","85","80"],
    ]

with open('student.csv','w',encoding='utf-8',newline='') as f:# newline='' 防止 Windows 下多出一行空行
    writer =csv.writer(f) # 创建一个 CSV 写入器
    writer.writerows(students)# 一次性写入多行，自动用逗号分隔

with open('student.csv','r',encoding='utf-8') as f:
    reader=csv.reader(f)# 创建一个 CSV 读取器
    header=next(reader)# 跳过表头（第一行）

    max_avg=0
    best_name=''
    
    for row in reader: # row 是列表，如 ["小明", "85", "92", "78"]
        name=row[0]
        chinese=int(row[1]) # CSV 读出来都是字符串，要转成数字
        math=int(row[2])
        english=int(row[3])

        total=chinese+math+english
        average=total/3


        print(f"{name}:语文{chinese},数学{math},英语{english},平均分{average:.2f}")

        if average>max_avg:
            max_avg=average
            best_name=name

    print(f"🏆 平均分最高：{best_name}({max_avg:.2f})")



##Note
##好问题！我帮你梳理一下 Python 中 CSV 需要掌握的核心知识点，按重要程度排序：
##
##  必须掌握 ⭐⭐⭐
##
##  1. 基本读写（上面已讲）
##
##  - csv.writer / csv.reader
##
##  2. csv.DictWriter 和 csv.DictReader（按列名操作）
##
##  import csv
##
##  # 用字典写入——更直观，不用记列索引
##  with open('student.csv', 'w', encoding='utf-8', newline='') as f:
##      fieldnames = ["姓名", "语文", "数学", "英语"]
##      writer = csv.DictWriter(f, fieldnames=fieldnames)
##      writer.writeheader()  # 自动写表头
##      writer.writerow({"姓名": "小明", "语文": "85", "数学": "92", "英语": "78"})
##      writer.writerow({"姓名": "小红", "语文": "90", "数学": "88", "英语": "95"})
##
##  # 用字典读取——通过列名访问，不用记 row[1] row[2]
##  with open('student.csv', 'r', encoding='utf-8') as f:
##      reader = csv.DictReader(f)
##      for row in reader:
##          print(f"{row['姓名']} 语文: {row['语文']}")  # 按列名取值，清晰多了
##
##  为什么要学这个？ 实际项目中列很多（20+列），用 row[0] row[15] 极易出错，用列名可读性好得多。
##
##  3. 分隔符变化
##
##  # 有些 CSV 用分号、制表符分隔（欧洲 Excel 导出的常见）
##  reader = csv.reader(f, delimiter=';')   # 分号分隔
##  reader = csv.reader(f, delimiter='\t')  # 制表符分隔（TSV）
##  writer = csv.writer(f, delimiter=';')
##
##  4. 数据类型转换
##
##  # CSV 读出来全部是字符串！这是最常见的坑
##  for row in reader:
##      score = int(row["语文"])      # 整数
##      price = float(row["价格"])    # 小数
##      is_pass = row["是否及格"] == "是"  # 布尔值
##
##  应该了解 ⭐⭐
##
##  5. 追加写入（不覆盖原文件）
##
##  with open('student.csv', 'a', encoding='utf-8', newline='') as f:  # 'a' 是追加
##      writer = csv.writer(f)
##      writer.writerow(["小李", "88", "91", "85"])
##
##  6. 处理含有逗号、换行的字段
##
##  # CSV 模块自动处理：如果字段包含逗号或换行，会自动加引号
##  # 比如 writerow(["小明", "喜欢语文,数学"]) → "小明","喜欢语文,数学"
##  # 读取时自动去掉引号，不用手动处理
##
##  7. 异常处理（文件不存在、格式错误）
##
##  try:
##      with open('student.csv', 'r', encoding='utf-8') as f:
##          reader = csv.reader(f)
##          for row in reader:
##              if len(row) != 4:  # 列数不对说明数据有问题
##                  print(f"跳过异常行: {row}")
##                  continue
##  except FileNotFoundError:
##      print("文件不存在，请先创建")
##
##  了解即可 ⭐
##  了解即可 ⭐
##
##  8. 自定义 quoting（引号策略）
##
##  # 所有字段都加引号
##  writer = csv.writer(f, quoting=csv.QUOTE_ALL)
##  # 只对非数字字段加引号
##  writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
##  # 不加引号（默认）
##  writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
