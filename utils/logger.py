import logging
import sys
from datetime import datetime
from config.settings import settings_frontend


_initialized = False    # 模块级全局变量，用于判断是否已经初始化过，被别的模块导入就能用，如果初始化过就不再重复初始化，避免重复日志


# level：日志级别，如 DEBUG、INFO、WARNING、ERROR
# log_dir：日志文件存放目录
def setup_logging(level=None, log_dir=None):
    """全局日志初始化，配置控制台 + 文件双输出。只执行一次。"""
    global _initialized
    if _initialized:    # 初始化过就不重复初始化
        return

    """
    level = level or settings_frontend.log_level：短路逻辑
        if level:
            使用 level
        else:
            使用配置文件
    """
    level = level or settings_frontend.log_level     # 若 level = None，则 setting_frontend.log_level 会被使用, 反之 level = level
    log_dir = log_dir or settings_frontend.log_dir

    log_level = getattr(logging, level, logging.INFO)   # 反射获取日志级别， logging.INFO: 代表一个整数，如 INFO 底层是一个值：20

    # 根 logger 配置
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 日志格式
    fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(fmt)
    root_logger.addHandler(console_handler)

    # 文件 handler
    log_dir.mkdir(parents=True, exist_ok=True)  # 不存在的目录就创建，parents 就是 mkdir -p 参数
    log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log" # logs/test_20260725_152030.log
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(fmt)
    root_logger.addHandler(file_handler)

    _initialized = True