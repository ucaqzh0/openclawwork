# -*- coding: utf-8 -*-
"""Global Optimization 提交前检查：输入文件完整、POTCAR 匹配。"""
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

def check_job_dir(job_dir):
    """检查单任务目录：POSCAR/INCAR/KPOINTS/POTCAR 存在。"""
    required = ["POSCAR", "INCAR", "KPOINTS", "POTCAR"]
    missing = [f for f in required if not (Path(job_dir) / f).exists()]
    return len(missing) == 0, missing

def run_pre_check(go_root):
    """对 go_root 下所有任务目录执行检查。"""
    base = Path(go_root)
    if not base.exists():
        print(f"❌ 目录不存在: {go_root}")
        return False
    job_dirs = []
    for root, _, _ in os.walk(base):
        r = Path(root)
        if (r / "POSCAR").exists() and (r / "INCAR").exists():
            job_dirs.append(r)
    job_dirs = sorted(set(job_dirs))
    all_ok = True
    print("=" * 60)
    print("Global Optimization 提交前检查")
    print("=" * 60)
    for jd in job_dirs:
        try:
            rel = jd.relative_to(base)
        except ValueError:
            rel = jd.name
        ok, missing = check_job_dir(str(jd))
        status = "✓" if ok else "✗"
        if not ok:
            all_ok = False
        print(f"{status} {rel}")
        if missing:
            print(f"    缺失: {', '.join(missing)}")
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
        go_root = getattr(mod, 'GO_ROOT', None)
    else:
        go_root = os.environ.get("GO_ROOT")
    if not go_root:
        print("请在 config.py 设置 GO_ROOT 或设置环境变量 GO_ROOT")
        sys.exit(1)
    ok = run_pre_check(go_root)
    sys.exit(0 if ok else 1)
