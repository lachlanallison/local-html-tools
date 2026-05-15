#!/usr/bin/env python3
import json, re

path = 'data/tools.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed = 0
for tool in data['tools']:
    s = tool.get('summary', '')
    s_orig = s
    
    # Remove control characters
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
    
    # Fix known corrupted summaries
    if tool['id'] == 'chrome-session-viewer':
        s = 'Parse Chrome session files in the browser\u2014tabs, groups, history\u2014with export. No data leaves your device.'
    
    if s != s_orig:
        tool['summary'] = s
        fixed += 1
        print(f'Fixed: {tool["id"]}')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Fixed {fixed} summaries. Total tools: {len(data["tools"])}')
