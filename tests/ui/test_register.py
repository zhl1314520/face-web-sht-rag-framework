import pytest

from pages.login_page import LoginPage
from pages.register_page import RegisterPage


""" 注册模块 """
@pytest.mark.parametrize("input_username, input_password, input_password_confirm, expected_success", [
    ("admin123456", "admin123456", "admin123456", True)
])
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

    assert page_register.is_return_to_login_page() == expected_success






