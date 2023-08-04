import json

with open(r'handlers/materials_for_studying/accents.json', encoding='UTF-8') as f:
    data = json.load(f)
for i in data:
    print(i)
