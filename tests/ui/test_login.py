import pytest
from pages.login_page import LoginPage
from utils.data_loader import load_test_data

""" UI 登录模块 """

login_data = load_test_data("ui_login.json")
# login_params = [tuple(d.values()) for d in login_data]
login_params = []
for data in login_data:
    login_params.append(tuple(data.values()))   # 得到("develop","123456",true),(),()...

@pytest.mark.parametrize("input_username, input_password, expected_success", login_params)
def test_login(driver, input_username, input_password, expected_success):
    page = LoginPage(driver)
    page.open()
    page.input_username(input_username)
    page.input_password(input_password)
    page.click_login_button()

    if expected_success:
        assert page.is_login_successful(), f"登录应成功, 用户名: {input_username}"
        page.logout()       # 只有登录成功才登出
    else:
        assert not page.is_login_successful(), f"登录应失败, 用户名: {input_username}"


