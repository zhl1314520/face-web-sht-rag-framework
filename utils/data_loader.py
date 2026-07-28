import json
from config.settings import settings_frontend

"""
加载测试数据，返回数据实例，而非 json
"""
def load_test_data(filename):
    """从 test_data 目录加载 JSON 测试数据，返回列表"""
    file_path = settings_frontend.test_data_dir / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f) # 误点：这里不是返回 json，而是返回[ {},{},{}...], ”反序列化“
