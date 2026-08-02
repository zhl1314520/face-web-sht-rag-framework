import pytest

from pages.register_page import RegisterPage
from utils.data_loader import load_test_data

""" 注册模块 """

register_data = load_test_data("ui_register.json")
# register_params = [tuple(d.values()) for d in register_data]
register_params = []
for data in register_data:
    register_params.append(tuple(data.values()))

@pytest.mark.parametrize("input_username, input_password, input_password_confirm, expected_success", register_params)
def test_register(driver, input_username, input_password, input_password_confirm, expected_success):
    page = RegisterPage(driver)
    page.open_login()
    page.click_register_button()

    assert page.is_redirect_to_register(), "点击注册按钮后应跳转到注册页"

    page.input_username(input_username)
    page.input_password(input_password)
    page.input_password_again(input_password_confirm)
    page.click_register_page_button()
    page.accept_alert()

    if expected_success:
        assert (page.is_return_to_login_page() and page.is_display_success_text()), f"注册成功后应返回登录页 and 显示成功信息, 用户名: {input_username}"
    else:
        assert not (page.is_return_to_login_page() or page.is_display_success_text()), f"注册失败(未返回登录页 or 未显示成功信息), 用户名: {input_username}"
