# -*- coding: utf-8 -*-
"""从 shared/config.py 加载配置，供各 tool 的 notebook 使用。"""
from pathlib import Path
import os
import importlib.util

def _find_config():
    env_root = os.environ.get("GO_CONFIG_DIR")
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
    cfg_path = _find_config()
    if cfg_path:
        spec = importlib.util.spec_from_file_location("config", cfg_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    class Default:
        GO_ROOT = "/home/ucaqzh0/thermol/100_water/absorption/absorption"
        DEFAULT_PARTITION = "young"
    return Default()
