#!/usr/bin/env python3
"""Read-only queue and job status; never submits or clears jobs."""
import argparse,json,urllib.request,urllib.parse
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8188');p.add_argument('--job');a=p.parse_args()
def get(path):
 with urllib.request.urlopen(a.url.rstrip('/')+path,timeout=10) as r:return json.load(r)
q=get('/queue')
print(json.dumps({k:[{'number':x[0],'prompt_id':x[1]} for x in q.get(k,[])] for k in ['queue_running','queue_pending']},indent=2))
if a.job:
 h=get('/history/'+urllib.parse.quote(a.job,safe='')).get(a.job,{})
 print(json.dumps({'prompt_id':a.job,'status':h.get('status'),'outputs':h.get('outputs')},indent=2))
