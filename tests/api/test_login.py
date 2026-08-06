import pytest

from utils.data_loader import load_test_data

""" API 登录模块 """

login_data = load_test_data("api_login.json")   # 获取测试数据
# login_params = [tuple(data.values()) for data in login_data]  # 列表推导式
login_params = []
for data in login_data:
    login_params.append(tuple(data.values()))

@pytest.mark.parametrize("username,password,expected_status_code", login_params)
def test_login(login_api, username, password, expected_status_code):
    result = login_api.login(username, password)
    result.assert_status_code(expected_status_code, f"登录接口状态码错误, 用户名: {username}")