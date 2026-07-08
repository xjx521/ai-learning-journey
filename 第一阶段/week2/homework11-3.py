import json

todos = [
   {"id": 1, "task": "学习 Python", "done": True},
    {"id": 2, "task": "写练习题", "done": False},
    {"id": 3, "task": "刷 LeetCode", "done": False},
    ]

with open('todos.json','w',encoding='utf-8') as f:
    json.dump(todos,f,ensure_ascii=False,indent=2)#ensure_ascii=False：正常显示中文，不会变成 \u 编码
                                                          #indent=2：JSON 文件自动换行缩进 2 空格，方便阅读

with open('todos.json','r',encoding='utf-8') as f:
    loaded=json.load(f)

    count_finish=0
    count_unfinish=0

    for row in loaded:
        if row['done']:
            count_finish+=1

        else:
            count_unfinish+=1

    print(f'任务完成数为：{count_finish}次')
    print(f'任务未完成数为：{count_unfinish}次')


