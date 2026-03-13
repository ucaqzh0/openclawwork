#!/usr/bin/env python3
import csv, subprocess, time, pathlib
track=pathlib.Path('/Users/zhenzezhao/.openclaw/workspace/memory/GR_dispatch_2026-03-13.tsv')
logp=pathlib.Path('/Users/zhenzezhao/.openclaw/workspace/memory/GR_migrator_2026-03-13.log')

def sh(cmd): return subprocess.check_output(cmd,shell=True,text=True).strip()

def ng_state(j):
  try:
    out=sh(f"ssh -o BatchMode=yes young.ng \"sacct -j {j} --format=State -n -P | head -n 1\"")
    return out.split()[0] if out else 'UNKNOWN'
  except: return 'UNKNOWN'

def young_pending(ids):
  if not ids: return []
  try: out=sh("ssh -o BatchMode=yes young \"qstat -u ucaqzh0 2>/dev/null\"")
  except: return []
  p=[]
  for ln in out.splitlines()[2:]:
    s=ln.split()
    if len(s)>=5 and s[0] in ids and s[4]=='qw': p.append(s[0])
  return p

def load():
  with open(track) as f: return list(csv.DictReader(f,delimiter='	'))

def save(rows):
  with open(track,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['task','cluster','jobid','state'],delimiter='	'); w.writeheader(); w.writerows(rows)

while True:
  rows=load(); changed=False; freed=0
  for r in rows:
    if r['cluster']=='young-ng' and r['state'] in ('SUBMITTED','RUNNING'):
      st=ng_state(r['jobid'])
      if st.startswith('RUNNING'):
        if r['state']!='RUNNING': r['state']='RUNNING'; changed=True
      elif st.startswith(('PENDING','CONFIGURING')):
        pass
      else:
        r['state']=st; changed=True; freed+=1

  if freed>0:
    ys=[r for r in rows if r['cluster']=='young' and r['state']=='SUBMITTED']
    pend=young_pending([r['jobid'] for r in ys])
    moved=0
    for _ in range(freed):
      cand=None
      for r in ys:
        if r['jobid'] in pend: cand=r; break
      if not cand: break
      subprocess.call(f"ssh -o BatchMode=yes young 'qdel {cand['jobid']} >/dev/null 2>&1 || true'",shell=True)
      newj=sh(f"ssh -o BatchMode=yes young.ng \"cd '{cand['task']}' && sbatch submit_SLURM_120_GR.sh\"").split()[-1]
      cand['cluster']='young-ng'; cand['jobid']=newj; cand['state']='SUBMITTED'; moved+=1; changed=True
      ys=[r for r in rows if r['cluster']=='young' and r['state']=='SUBMITTED']
      pend=young_pending([r['jobid'] for r in ys])
    if moved:
      with open(logp,'a') as lf: lf.write(f"[{time.strftime('%F %T')}] moved {moved} young->young-ng\n")

  if changed: save(rows)
  time.sleep(120)
