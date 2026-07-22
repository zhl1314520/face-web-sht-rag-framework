from conftest import pause
from pages.product_page import ProductPage
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import settings_frontend

""" 项目模块 """


def test_product_create_button(driver, general_login, expected_success = True):
    page = ProductPage(driver)
    page.open()
    page.click(page.product_create_button)

    assert page.is_click_create_product_button_success() == expected_success

@pytest.mark.parametrize("name, description, price, expected_success", [
    ("Test Product2", "This is a test product.", "2", True),
])
def test_product2_function_button(driver, general_login, expected_success, name, description, price):
    page = ProductPage(driver)
    page.open()
    page.click(page.product_view2)

    assert page.is_view2_success() == expected_success

    page.click(page.view2_edit)

    assert page.is_access_edit_product2_success() == expected_success

    page.clean_inputs()
    page.input_product_details(name, description, price)
    page.click(page.update_button)

    assert page.is_update_product_success() == expected_success

    page.click(page.delete_button)
    page.click(page.cancel_delete)

    assert page.is_return_products_main_page() == expected_success

    page.click(page.import_JSON_button)

    assert page.is_access_import_JSON_page_success() == expected_success

    # "实际的 products.json 路径"
    page.input(page.browse, str(settings_frontend.import_json_file))
    page.click(page.submit_import_button)

    assert page.is_import_JSON_success() == expected_success



