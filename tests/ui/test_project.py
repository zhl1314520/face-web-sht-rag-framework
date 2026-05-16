from conftest import pause
from pages.project_page import ProjectPage
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" 项目模块 """
# @pytest.mark.parametrize("input_project_name, expected_success", [
#     ("test_by_delete", True),
#     ("17201665342@163.com", False),
#     ("10293832823@163.com", False)
# ])
# def test_project_input(driver, input_project_name, general_login, expected_success):
#     page = ProjectPage(driver)
#     # 添加等待，确保登录后跳转到 dashboard
#     WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
#     page.open()
#     page.input_project_name(input_project_name)
#
#     assert page.is_search_project_success() == expected_success
#
# def test_project_scroll(driver, general_login, expected_success = True):
#     page = ProjectPage(driver)
#     WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
#     page.open()
#     page.scroll_page(10, 0.01)
#
#     assert page.is_reach_bottom() == expected_success


def test_project_create_button(driver, expected_success = True):
    page = ProjectPage(driver)
    page.open()
    page.click(page.project_create_button)
    pause(2)

    assert page.is_click_create_project_button_success() == expected_success