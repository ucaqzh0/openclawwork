#!/usr/bin/env python3
import csv, subprocess, time, pathlib
track = pathlib.Path("/Users/zhenzezhao/.openclaw/workspace/memory/go1body_batch_dispatch_2026-03-13.tsv")
logp = pathlib.Path("/Users/zhenzezhao/.openclaw/workspace/memory/go1body_batch_migrator_2026-03-13.log")

def sh(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def ng_state(jobid):
    try:
        out=sh(f"ssh -o BatchMode=yes young.ng \"sacct -j {jobid} --format=State -n -P | head -n 1\"")
        return out.split()[0] if out else 'UNKNOWN'
    except:
        return 'UNKNOWN'

def young_pending(jobids):
    if not jobids: return []
    try:
        out=sh("ssh -o BatchMode=yes young \"qstat -u ucaqzh0 2>/dev/null\"")
    except:
        return []
    p=[]
    for ln in out.splitlines()[2:]:
        s=ln.split()
        if len(s)>=5 and s[0] in jobids and s[4]=='qw': p.append(s[0])
    return p

def load():
    with open(track) as f: return list(csv.DictReader(f, delimiter='	'))

def save(rows):
    with open(track,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['task','cluster','jobid','state'],delimiter='	'); w.writeheader(); w.writerows(rows)

while True:
    rows=load(); changed=False; freed=0
    for r in rows:
        if r['cluster']=='young-ng' and r['state'] in ('SUBMITTED','RUNNING'):
            st=ng_state(r['jobid'])
            if st.startswith('RUNNING'): r['state']='RUNNING'; changed=True
            elif st.startswith(('PENDING','CONFIGURING')): pass
            else:
                r['state']=st; changed=True; freed += 1

    if freed>0:
        y=[r for r in rows if r['cluster']=='young' and r['state']=='SUBMITTED']
        pend=young_pending([r['jobid'] for r in y])
        moved=0
        for _ in range(freed):
            cand=None
            for r in y:
                if r['jobid'] in pend: cand=r; break
            if not cand: break
            subprocess.call(f"ssh -o BatchMode=yes young 'qdel {cand['jobid']} >/dev/null 2>&1 || true'", shell=True)
            newjid=sh(f"ssh -o BatchMode=yes young.ng \"cd '{cand['task']}' && sbatch submit_SLURM_120_batch.sh\"").split()[-1]
            cand['cluster']='young-ng'; cand['jobid']=newjid; cand['state']='SUBMITTED'; moved += 1; changed=True
            y=[r for r in rows if r['cluster']=='young' and r['state']=='SUBMITTED']
            pend=young_pending([r['jobid'] for r in y])
        if moved:
            with open(logp,'a') as lf: lf.write(f"[{time.strftime('%F %T')}] moved {moved} tasks young->young-ng\n")

    if changed: save(rows)
    time.sleep(120)
