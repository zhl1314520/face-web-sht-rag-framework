from conftest import pause
from pages.product_page import ProductPage
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" 项目模块 """


def test_product_create_button(driver, expected_success = True):
    page = ProductPage(driver)
    page.open()
    page.click(page.product_create_button)
    pause(2)

    assert page.is_click_create_product_button_success() == expected_success

@pytest.mark.parametrize("name, description, price, expected_success", [
    ("Test Product1", "This is a test product.", "2", True),
])
def test_product_view(driver, general_login, expected_success, name, description, price):
    page = ProductPage(driver)
    page.open()
    pause(2)
    page.click(page.product_view)
    pause(2)

    assert page.is_view_success() == expected_success

    page.click(page.view1_products)
    pause(2)

    assert page.is_return_products_main_page() == expected_success

    page.click(page.product_view)
    page.click(page.view1_edit)
    page.input_product_details(name, description, price)
    pause(5)




