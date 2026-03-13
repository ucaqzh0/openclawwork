#!/bin/bash
set -euo pipefail
LOG=/Users/zhenzezhao/.openclaw/workspace/monitor_bridge_then_cancel_slurm.log
echo "[$(date)] started" >> "$LOG"
while true; do
  if ssh young 'qstat -u ucaqzh0 2>/dev/null | egrep "BRIDGE_(CO|COOH|CHO)" | egrep " r " -q'; then
    echo "[$(date)] bridge job running on young, cancel slurm GO jobs 3351 3352 3353" >> "$LOG"
    ssh young.ng 'scancel 3351 3352 3353 || true; squeue -u ucaqzh0 -o "%.18i %.20j %.10T" | egrep "GO_CO|GO_COOH|GO_CHO|JOBID" || true' >> "$LOG" 2>&1
    break
  fi
  sleep 30
done
echo "[$(date)] monitor exit" >> "$LOG"
