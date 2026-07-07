import json

students = [
      {"name": "小明", "score": 92},
      {"name": "小红", "score": 76},
      {"name": "小刚", "score": 58},
      {"name": "小美", "score": 85},
  ]

with open ("students.json",'w',encoding="utf-8") as f:#'w'=写
    json.dump(students,f,ensure_ascii=False)

with open("students.json",encoding="utf-8") as f:#读
    loaded=json.load(f)

#额外挑战
#for s in loaded:
    
#    s['grade']='A' if s['score']>=80 else'B' if 60<=s['score']<80 else'C' 

#print(loaded)

good=map(lambda x: x['name'],filter(lambda x:x['score']>=80,loaded))

print("优秀学生：",list(good))

##json

### import json

#  data = {"name": "Alice", "score": 85}   # 一个 Python 字典

  # 1. 字典 → JSON 字符串（dumps：dump string）
#  s = json.dumps(data)         # '{"name": "Alice", "score": 85}'
#  print(s, type(s))            # <class 'str'>

  # 2. JSON 字符串 → 字典（loads：load string）
#  d = json.loads(s)            # 又变回字典
#  print(d["name"])             # Alice

  # 3. 存到文件（dump：不带 s，直接写文件）
#  with open("a.json", "w", encoding="utf-8") as f:
#      json.dump(data, f)

  # 4. 从文件读（load：不带 s，直接读文件）
# with open("a.json", encoding="utf-8") as f:
#     d2 = json.load(f)

#  ▎ 记忆口诀:带 s 的操作字符串,不带 s 的操作文件。dumps/loads 中间多了个 s = string。
