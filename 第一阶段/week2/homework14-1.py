### Day 14：综合项目——命令行记账本 ⭐⭐⭐⭐⭐

from datetime import *
import json
information=[]
next_id=1

try:
    with open('notebook.json', 'r', encoding='utf-8') as f:
        information=json.load(f)
    if information:
        next_id=max(i['id'] for i in information)+1
except FileNotFoundError:
    pass

while True:
    print('===== 💰 个人记账本 =====')
    print("""
            1. 记一笔
            2. 查看所有
            3. 按类别筛选
            4. 删除记录
            5. 统计汇总
            0. 退出
    """)

    try:
        user_choices=int(input('请选择操作：'))
    except ValueError:
        print('请输入0-5的整数执行操作')
        continue#如果没有 continue，use_choices未定义,代码继续往下走！

    if user_choices==1:
        print('===== 记一笔 =====')

        record={}
        #用户自行输入
        record['type']=input('收入还是支出？')

        try:
            record['amount']=float(input('金额：'))
        except ValueError:
            print('输入的金额应该为小数！')
            continue
        record['category']=input('类别（餐饮/交通/购物/工资/其他）：')
        record['note']=input('备注：')
        record['date']=input('日期（回车默认今天）：')
        #日期
        if record['date']=='':
            record['date']=str(date.today())

        #id
        record['id']=next_id
        next_id+=1

        information.append(record)
        print(f'✅ 已记录：{record['type']}|{record['amount']}元|{record['category']}|{record['note']}')
    elif user_choices==2:
        print('===== 查看所有 =====')

        if len(information)==0:
            print('暂无数据')
        else:
            for i in information:
                    print(f'ID:{i['id']}|{i['type']}|{i['amount']}元|{i['category']}|{i['note']}|{i['date']}')
            print()
    
    elif user_choices==3:
        print('===== 按类别筛选 =====')
        search=input('请输入要搜索的类别（餐饮/交通/购物/工资/其他）：')
        found =False

        if len(information)==0:
            print('暂无数据')
        else:
            for i in information:
                if i['category'].strip()==search.strip():
                    print(f'ID:{i['id']}|{i['type']}|{i['amount']}元|{i['category']}|{i['note']}|{i['date']}')
                    found=True
            print()
            if not found:
                print('没有找到该类别的记录！')
    elif user_choices==4:
        print('===== 删除记录 =====')

        try:
            delete=int(input('请输入要删除的记录id:'))
        except ValueError:
            print('输入整数id！')
            continue
        found=False
        target_index=-1
        
        if len(information)==0:
            print('暂无数据')
        else:
            for i in information:
                if delete==i['id']:
                    target_index=information.index(i)
                    found=True
                    break
            if not found:
                print('该记录不存在')
            else:
                del information[target_index]
                print('删除成功！')

    elif user_choices==5:
        gross_wages=0
        payroll=0
        food=traffic=shopping=pay_other=0
        wage=wage_other=0
        if len(information)==0:
            print('暂无数据')
        else:
            for i in information:
                if i['type']=='收入':
                    gross_wages+=i['amount']
                    if i['category']=='工资':
                        wage+=i['amount']
                    else:
                        wage_other+=i['amount']
                    
                else:
                    payroll+=i['amount']
                    if i['category']=='餐饮':
                        food+=i['amount']
                    elif i['category']=='交通':
                        traffic+=i['amount']
                    elif i['category']=='购物':
                        shopping+=i['amount']
                    else:
                        pay_other+=i['amount']
            
            print(f"""
                    ===== 统计汇总 =====
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
            
    elif user_choices==0:
        with open('notebook.json','w',encoding='utf-8') as f:
            json.dump(information,f)
        break

    else:
        print('操作不正确！请重新输入')
