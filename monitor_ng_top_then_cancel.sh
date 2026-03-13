#!/bin/bash
set -euo pipefail
LOG=/Users/zhenzezhao/.openclaw/workspace/monitor_ng_top_then_cancel.log
JOBS="3351 3352 3353"
TOP_DIRS=(
"/home/ucaqzh0/thermol/precursor_generation/absorption/1_body/GO/absorption_single_CO/job_POSCAR_CO_top"
"/home/ucaqzh0/thermol/precursor_generation/absorption/1_body/GO/absorption_single_COOH/job_POSCAR_COOH_top"
"/home/ucaqzh0/thermol/precursor_generation/absorption/1_body/GO/absorption_single_CHO/job_POSCAR_CHO_top"
)

echo "[$(date)] monitor started: wait until any NG TOP starts, then scancel $JOBS" >> "$LOG"
while true; do
  started=0
  for d in "${TOP_DIRS[@]}"; do
    if ssh young.ng "[ -s '$d/OUTCAR' ] || [ -s '$d/OSZICAR' ] || ls '$d'/result.* >/dev/null 2>&1"; then
      started=1
      hit="$d"
      break
    fi
  done
  if [ "$started" -eq 1 ]; then
    echo "[$(date)] detected TOP started at $hit" >> "$LOG"
    ssh young.ng "scancel $JOBS || true; squeue -u ucaqzh0 -o '%.18i %.20j %.10T %.10M' | egrep '3351|3352|3353|JOBID' || true" >> "$LOG" 2>&1
    echo "[$(date)] canceled NG GO jobs" >> "$LOG"
    break
  fi
  sleep 20
done
