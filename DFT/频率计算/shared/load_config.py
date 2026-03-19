# -*- coding: utf-8 -*-
"""从 shared/config.py 加载配置，供各 tool 的 notebook 使用。"""
from pathlib import Path
import os
import importlib.util

def _find_config():
    """从 cwd 向上查找 频率计算/shared/config.py；或使用 XIAOZHUA_FREQ_DIR 环境变量"""
    env_root = os.environ.get("XIAOZHUA_FREQ_DIR")
    if env_root:
        cfg = Path(env_root) / "shared" / "config.py"
        if cfg.exists():
            return cfg
    p = Path.cwd()
    while p != p.parent:
        cfg = p / "shared" / "config.py"
        if cfg.exists():
            return cfg
        p = p.parent
    return None

def load_config():
    """加载 ZPE_ROOT、DEFAULT_PARTITION 等。返回命名空间。"""
    cfg_path = _find_config()
    if cfg_path:
        spec = importlib.util.spec_from_file_location("config", cfg_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    # 回退默认
    class Default:
        ZPE_ROOT = "/home/ucaqzh0/thermol/100_water/absorption/absorption/ZPE/high/"
        DEFAULT_PARTITION = "young"
    return Default()
