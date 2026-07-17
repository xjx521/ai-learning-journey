### Day 20：综合项目——用面向对象重构记账本 ⭐⭐⭐⭐⭐

import json
from datetime import *
from enum import Enum


class Record:  # `Record` 类（或用 dataclass）：表示一条记录
    def __init__(
        self,
        record_id: int,
        type: str,
        category: str,
        amount: float,
        note: str,
        record_date: str = None,
    ):
        self.id = record_id
        self.type = type
        self.category = category
        self.amount = amount
        self.note = note
        self.date = record_date or str(date.today())

    def __str__(self):
        return f"ID:{self.id}|{self.type}|{self.amount}元|{self.category}|{self.note}|{self.date}"


class Category(Enum):  # `Category` 枚举：表示类别（餐饮/交通/购物/工资/其他）
    FOOD = "餐饮"
    TRAFFIC = "交通"
    SHOPPING = "购物"
    WAGE = "工资"
    OTHER = "其他"


class AccountBook:  # `AccountBook` 类：管理所有记录（增删改查、统计）
    def __init__(self, filename="records.json"):
        self.records = []  # 存储对象 里面是对象，不是字典
        self.filename = filename
        self.next_id = 1
        self.load()

    def load(self):  # 读取 load() │ 字典 → Record对象 读取的是字典
        try:
            with open("records.json", "r", encoding="utf-8") as f:
                data = json.load(f)  # 读取字典
        except (FileNotFoundError, json.JSONDecodeError):
            return  # 文件不存在时，直接 return，不要继续往下走

        for item in data:
            # 把每个字典转成 Record 对象
            record = Record(
                record_id=item["id"],
                type=item["type"],
                category=item["category"],
                amount=item["amount"],
                note=item["note"],
                record_date=item["date"],
            )
            self.records.append(record)  # 把record对象添加到列表
        if self.records:
            self.next_id = max(i.id for i in self.records) + 1

    def save(self):  # 保存 save() │ Record对象 → 字典 写入文件
        data = []  # 存放字典
        for record in self.records:
            record = {
                "id": record.id,
                "type": record.type,
                "category": record.category,
                "amount": record.amount,
                "note": record.note,
                "date": record.date,
            }  # 把类变成字典
            data.append(record)

        with open("records.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, type, category, amount, note, date=None):  # 添加记录
        record = Record(
            self.next_id, type, category, amount, note, date
        )  # 创建Record对象
        self.records.append(record)  # 把对象添加到列表
        self.next_id += 1
        print("✅ 已记录")
        print(self.records[-1])
        return record

    def delete(self, target_id):  # 删除记录
        found = False
        target_index = -1
        if self.records:
            for i in self.records:
                if target_id == i.id:
                    target_index = self.records.index(i)
                    found = True
            if not found:
                print("该记录不存在！")
            else:
                del self.records[target_index]
                print("✅删除成功")

    def search(self, keyword):  # 按类别筛选
        found = False
        if self.records:
            for i in self.records:
                if keyword.strip() == i.category.strip():
                    print(i)
                    found = True
        if not found:
            print("没有找到该类别记录！")

    def update(self, record_id, **kwargs):  # 更新记录
        found = False
        if self.records:
            for i in self.records:
                if record_id == i.id:
                    found = True
                    if "type" in kwargs:
                        i.type = kwargs["type"]
                    if "category" in kwargs:
                        i.category = kwargs["category"]
                    if "amount" in kwargs:
                        i.amount = kwargs["amount"]
                    if "note" in kwargs:
                        i.note = kwargs["note"]
                    if "date" in kwargs:
                        i.date = kwargs["date"]
                    print("✅更新成功!")
                    print(i)
            if not found:
                print("该条记录不存在！")

    def get_all(self):  # 查看所有
        if self.records:
            for i in self.records:
                print(i)
                print()
        else:
            print("暂无数据！")

    def get_by_id(self, target_id):  # 按ID查找
        found = False
        if self.records:
            for i in self.records:
                if i.id == target_id:
                    print(i)
                    found = True
            if not found:
                print("该条记录不存在！")

    def summary(self):  # 统计汇总
        gross_wages = 0
        payroll = 0
        wage = wage_other = 0
        food = traffic = shopping = pay_other = 0

        if self.records:
            for i in self.records:
                if i.type == "收入":
                    gross_wages += i.amount
                    if i.category == "工资":
                        wage += i.amount
                    else:
                        wage_other += i.amount

                else:
                    payroll += i.amount
                    if i.category == "餐饮":
                        food += i.amount
                    elif i.category == "交通":
                        traffic += i.amount
                    elif i.category == "购物":
                        shopping += i.amount
                    else:
                        pay_other += i.amount

            print(f"""
总收入：{gross_wages} 元
总支出：{payroll} 元
结余：{gross_wages-payroll} 元
                    """)
            print(f"""
按类别支出：
    餐饮：{food} 元
    交通：{traffic} 元
    购物：{shopping}元
    其他：{pay_other}元
                      """)
            print(f"""
按类别收入：
    工资：{wage}元
    其他：{wage_other}元
                    """)


if __name__ == "__main__":
    book = AccountBook()

    while True:
        print("===== 💰 个人记账本 =====")
        print("""
            1. 记一笔
            2. 查看所有
            3. 按类别筛选
            4. 按ID查找
            5. 更新记录
            6. 删除记录
            7. 统计汇总
            0. 退出
             """)

        try:
            user_choices = int(input("请选择操作："))
        except ValueError:
            print("请输入相应的值来进行操作！")
            continue

        if user_choices == 1:
            print("===== 记一笔 =====")

            type = input("收入还是支出？")
            try:
                amount = float(input("请输入金额："))
            except ValueError:
                print("输入的金额应该为小数！")
                continue
            category = input("类别（餐饮/交通/购物/工资/其他）：")
            note = input("备注：")
            book.add(type, category, amount, note)

        elif user_choices == 2:
            print("===== 查看所有 =====")
            book.get_all()

        elif user_choices == 3:
            print("===== 按类别筛选 =====")
            keyword = input("请输入要搜索的类别（餐饮/交通/购物/工资/其他）：")
            book.search(keyword)

        elif user_choices == 4:
            print("===== 按id查找 =====")
            try:
                target_id = int(input("请输入要搜索的记录ID："))
            except ValueError:
                print("目标ID应该为整数！")
                continue
            book.get_by_id(target_id)

        elif user_choices == 5:
            print("===== 更新记录 =====")
            try:
                record_id = int(input("请输入要删除的记录ID："))
            except ValueError:
                print("目标ID应该为整数！")
                continue

            field = input("请输入要更新的内容（type/amount/category/note/date）：")
            value = input("新值：")
            # 用字典 + ** 解包
            if field == "amount":  # 如果金额，要转成浮点数
                value = float(value)

            kwargs = {field: value}
            book.update(record_id, **kwargs)

        elif user_choices == 6:
            print("===== 删除记录 =====")
            try:
                target_id = int(input("请输入要删除的记录ID："))
            except ValueError:
                print("目标ID应该为整数！")
                continue

            book.delete(target_id)

        elif user_choices == 7:
            print("===== 统计汇总 =====")
            book.summary()

        elif user_choices == 0:
            print("===== 退出 =====")
            book.save()
            print("✅记账成功")
            break
