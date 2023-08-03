import json

with open(r'materials_for_studing/accents.json', encoding='UTF-8') as f:
    data = json.load(f)
for i in data:
    print(i)
