import pytest
import time
import random
from utils.data_loader import load_test_data

""" API 注册模块 """

# 为正向用例（期望302）的用户名追加日期时间+随机数，避免重复注册
_ensure_unique_username = time.strftime("%m%d%H%M%S") + str(random.randint(10, 99)) # 加时间戳和随机的两位数

register_data = load_test_data("api_register.json")
register_params = []
for data in register_data:
    values = list(data.values())
    if data["expected_status_code"] == 302:
        values[0] = values[0] + _ensure_unique_username        # 用户名追加唯一后缀
    register_params.append(tuple(values))

# 后续登录的 username 只能是 username + 时间戳 + 随机数，才能登录成功，由于加了时间戳和随机数，api_register.json 文件内容可以不用改一直测
@pytest.mark.parametrize("username,password1,password2, expected_status_code", register_params)
def test_register(register_api, username, password1, password2, expected_status_code):
    result = register_api.register(username, password1, password2)
    result.assert_status_code(expected_status_code, f"注册接口状态码错误, 用户名: {username}")
