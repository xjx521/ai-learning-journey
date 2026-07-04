#### 题目 5：综合——学生成绩管理系统（命令行版）⭐⭐⭐⭐

all_students=[]


while True:
    print("""===== 学生成绩管理系统 =====
1. 添加学生
2. 查看所有学生
3. 查找学生
4. 删除学生
5. 统计平均分
0. 退出""")
    control=int(input("请选择操作："))
    
    if control==1:#1. 添加学生
        
        student={}
        student["id"]=input("请输入学生id：")
        student["name"]=input("请输入学生姓名：")
        student["score"]=int(input("请输入学生成绩："))
        #student={"id":id,"name":name,"score":score}
        all_students.append(student)
        print(f"✅ 已添加：{student["name"]}-{student["score"]}分")

    elif control==2:#2. 查看所有学生
        if len(all_students)==0:
            print("暂无数据")
        else:
            print("=== 所有学生 ===")
            print("学号","姓名","成绩",end=" ")
            print()
            for i in all_students:
                for each in i:#：Python 中直接 for x in 字典，默认只遍历键（key），所以 each 依次是 "id"、"name"、"score" ——这就是为什么只显示名称不显示数据。
                    print(i[each],end=" ")# ← 用 i[each] 来取值，而不是打印 each
                print()

    elif control==3:#查找学生
        search=input("请输入要查找的学生姓名：")
        found=False
        for j in all_students: #j = {"id":"1", "name":"张三", "score":"90"} ← j 是一个字典
                if search==j["name"]:
                    print(f"该学生信息为：ID={j['id']}, 姓名={j['name']}, 成绩={j['score']}")## ❌ all_students 是列表，列表只能用数字索引，不能用字典当索引！
                    found=True
        if not found:
                    print("该学生不存在")

    elif control==4:#4. 删除学生
        delete=input("请输入要删除的学生姓名：")
        found=False#避免重复打印该学生未存在
        target_index=-1
        for k in all_students:
            if delete==k["name"]:
                target_index=all_students.index(k)# ← 找到后记录位置
                found=True
                break

        if not found:
                print("该学生不存在")
        else:
            del all_students[target_index]# ← 循环外执行删除，避免导致索引错乱
            print("删除成功")
        

    elif control==5:

            if len(all_students) == 0:
                print("暂无学生")
            else:
                total=0
                for j in all_students:
                    total+=j['score']
                average=total/len(all_students)#：sum() 只能接收一个"一堆东西的集合"（可迭代对象，比如列表 [80, 90,70]）
                print(f"全班平均分：{average:.1f}") #保留一位小数

    elif control==0:
        break

    else:
        print("操作不存在，请重新选择！")


