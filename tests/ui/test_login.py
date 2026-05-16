import pytest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

""" 登录模块 """
@pytest.mark.parametrize("input_username, input_password, expected_success", [
    ("admin", "zxcvbnm", True),
    ("", "123456", False),
    ("developer", "", False),
    ("developers", "123456", False),
    ("developer", "1123456", False),
    ("", "", False),
])
def test_login(driver, input_username, input_password, expected_success):
    page = LoginPage(driver)
    page.open()
    page.input_username(input_username)
    page.input_password(input_password)
    page.click_login_button()

    assert page.is_login_successful() == expected_success




