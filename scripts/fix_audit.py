#!/usr/bin/env python3
import json

path = 'data/tools.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remove tools
removed = []
data['tools'] = [t for t in data['tools'] if t['id'] not in ('minifier-org', 'simonwillison-tools') or removed.append(t['id'])]
print(f'Removed: {removed}')

# Fix offline flags
for t in data['tools']:
    if t['id'] == 'qr':
        t['runtime']['offline'] = 'yes'
        print(f'Fixed qr: partial -> yes')
    elif t['id'] == 'webcam-tester':
        t['runtime']['offline'] = 'yes'
        print(f'Fixed webcam-tester: partial -> yes')
    elif t['id'] == 'svg-render':
        t['runtime']['offline'] = 'yes'
        print(f'Fixed svg-render: partial -> yes')

data['meta']['version'] = 4

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Total tools: {len(data["tools"])}')
