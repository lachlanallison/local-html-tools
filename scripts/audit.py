#!/usr/bin/env python3
import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'{"ID":30s} {"SF":3s} {"Offline":10s} {"Net":5s} {"Name"}')
print('-' * 80)
for t in data['tools']:
    r = t['runtime']
    print(f'{t["id"]:30s} {str(r["single_file"]):3s} {r["offline"]:10s} {str(r.get("needs_network","?")):5s} {t["name"]}')
