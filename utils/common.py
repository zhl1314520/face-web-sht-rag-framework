"""通用工具类：文件操作、加密解密、时间处理"""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path


# ======
# 文件操作
# ======
def read_json(file_path):
    """读取 JSON 文件"""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f) # 返回的是对象，list/dict


def write_json(file_path, data):
    """写入 JSON 文件"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)    # ensure_ascii=False：中文不乱码，indent=2：控制输出JSON数据的缩进空格数


def ensure_dir(dir_path):
    """确保目录存在"""
    Path(dir_path).mkdir(parents=True, exist_ok=True)


# ======
# 加密解密
# ======
def md5(text):
    """加密，计算字符串的 MD5 哈希值"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sha256(text):
    """解密，计算字符串的 SHA256 哈希值"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ======
# 时间处理
# ======
# def timestamp():
#     """返回当前时间戳（秒）"""
#     return int(time.time())


def datetime_str(fmt="%Y-%m-%d %H:%M:%S"):
    """返回格式化的当前时间字符串"""
    return datetime.now().strftime(fmt)


def datetime_filename():
    """返回适合用于文件名的时间字符串，如 20260721_153000"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
