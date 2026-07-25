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
    page_login = RegisterPage(driver)
    page_login.open_login()
    page_login.click_register_button()

    assert page_login.is_redirect_to_register() == True

    page_register = RegisterPage(driver)
    page_register.input_username(input_username)
    page_register.input_password(input_password)
    page_register.input_password_again(input_password_confirm)
    page_register.click_register_page_button()
    page_register.accept_alert()

    assert page_register.is_return_to_login_page() == expected_success
