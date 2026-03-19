# -*- coding: utf-8 -*-
"""频率计算提交前检查：原子固定、INCAR。可独立运行或由 notebook 调用。"""
import os
import sys
from pathlib import Path

def _find_config():
    p = Path.cwd()
    while p != p.parent:
        cfg = p / "shared" / "config.py"
        if cfg.exists():
            return cfg
        p = p.parent
    return None

def check_cu_fixed(poscar_path):
    """检查 POSCAR 中 Cu 基底原子是否全部固定。"""
    if not os.path.exists(poscar_path):
        return False, "无 POSCAR"
    with open(poscar_path, 'r') as f:
        lines = f.readlines()
    if len(lines) < 8 or "Selective dynamics" not in ''.join(lines):
        return False, "无 Selective dynamics"
    el = lines[5].strip().split()
    num = lines[6].strip().split()
    if not el or el[0].upper() != 'CU':
        return True, "无 Cu 基底（跳过）"
    cu_count = int(num[0])
    coord_start = next((i for i, l in enumerate(lines) if "Selective dynamics" in l), -1) + 2
    if coord_start < 2:
        return False, "格式异常"
    for i in range(coord_start, min(coord_start + cu_count, len(lines))):
        parts = lines[i].split()
        if len(parts) >= 6 and not (parts[3].upper() == 'F' and parts[4].upper() == 'F' and parts[5].upper() == 'F'):
            return False, f"Cu 原子 {i - coord_start + 1} 未固定"
    return True, "OK"

def check_incar(incar_path):
    """检查 INCAR 存在且含关键参数。"""
    if not os.path.exists(incar_path):
        return False, "无 INCAR"
    text = open(incar_path).read()
    required = ["IBRION", "ISIF", "NSW"]
    for r in required:
        if r not in text:
            return False, f"缺少 {r}"
    return True, "OK"

def run_pre_check(zpe_root):
    """对 zpe_root 下所有任务目录执行检查，打印结果。"""
    base = Path(zpe_root)
    if not base.exists():
        print(f"❌ 目录不存在: {zpe_root}")
        return False
    job_dirs = []
    for root, _, _ in os.walk(base):
        r = Path(root)
        if (r / "POSCAR").exists() and (r / "INCAR").exists():
            job_dirs.append(r)
    job_dirs = sorted(set(job_dirs))
    all_ok = True
    print("=" * 60)
    print("提交前检查")
    print("=" * 60)
    for jd in job_dirs:
        try:
            rel = jd.relative_to(base)
        except ValueError:
            rel = jd.name
        poscar = jd / "POSCAR"
        incar = jd / "INCAR"
        ok_cu, msg_cu = check_cu_fixed(str(poscar))
        ok_inc, msg_inc = check_incar(str(incar))
        status = "✓" if (ok_cu and ok_inc) else "✗"
        if not (ok_cu and ok_inc):
            all_ok = False
        print(f"{status} {rel}")
        if not ok_cu:
            print(f"    原子固定: {msg_cu}")
        if not ok_inc:
            print(f"    INCAR: {msg_inc}")
    print("=" * 60)
    if all_ok:
        print("✔ 全部通过，可提交")
    else:
        print("✗ 存在未通过项，禁止提交")
    return all_ok

if __name__ == "__main__":
    cfg_path = _find_config()
    if cfg_path:
        spec = __import__('importlib.util').spec_from_file_location("config", cfg_path)
        mod = __import__('importlib.util').module_from_spec(spec)
        spec.loader.exec_module(mod)
        zpe_root = getattr(mod, 'ZPE_ROOT', None)
    else:
        zpe_root = os.environ.get("ZPE_ROOT")
    if not zpe_root:
        print("请在 config.py 设置 ZPE_ROOT 或设置环境变量 ZPE_ROOT")
        sys.exit(1)
    ok = run_pre_check(zpe_root)
    sys.exit(0 if ok else 1)
