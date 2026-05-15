#!/usr/bin/env python3
import json

path = 'data/tools.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for t in data['tools']:
    if t['id'] == 'transparent-png':
        t['runtime']['offline'] = 'yes'
        print(f'Fixed: {t["id"]} partial -> yes')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Done')
