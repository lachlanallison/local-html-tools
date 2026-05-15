#!/usr/bin/env python3
"""Check all tool URLs return 200."""
import json, urllib.request, urllib.error, sys

path = 'data/tools.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

bad = []
for t in data['tools']:
    url = t['url']
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        resp = urllib.request.urlopen(req, timeout=10)
        code = resp.getcode()
        if code >= 400:
            bad.append((t['id'], url, code))
            print(f'BAD {code} {t["id"]:30s} {url}')
        else:
            print(f'OK  {code} {t["id"]:30s} {url}')
    except urllib.error.HTTPError as e:
        bad.append((t['id'], url, e.code))
        print(f'BAD {e.code} {t["id"]:30s} {url}')
    except Exception as e:
        bad.append((t['id'], url, str(e)))
        print(f'ERR {t["id"]:30s} {url} -> {e}')

if bad:
    print(f'\n{len(bad)} FAILED URLS:')
    for tid, url, reason in bad:
        print(f'  {tid:30s} {reason} {url}')
    sys.exit(1)
else:
    print(f'\nAll {len(data["tools"])} URLs OK')
