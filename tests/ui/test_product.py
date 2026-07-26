from conftest import pause
from pages.product_page import ProductPage
import pytest
from config.settings import settings_frontend
from utils.data_loader import load_test_data
from utils.soft_assert import SoftAssert

""" UI 项目模块 """

product_data = load_test_data("ui_product.json")
# product_params = [tuple(data.values()) for data in product_data]
# 参数列表
product_params = []
for data in product_data:
    product_params.append(tuple(data.values()))


def test_product_create_button(driver, general_login, expected_success = True):
    page = ProductPage(driver)
    page.open()
    page.click(page.product_create_button)

    assert page.is_click_create_product_button_success(), "点击创建产品按钮后应成功进入创建页"

@pytest.mark.parametrize("name, description, price, expected_success", product_params)
def test_product2_function_button(driver, general_login, expected_success, name, description, price):
    soft_assert = SoftAssert()
    page = ProductPage(driver)
    page.open()
    page.click(page.product_view2)

    soft_assert.assert_true(page.is_view2_success(), "查看产品详情应成功")

    page.click(page.view2_edit)
    soft_assert.assert_true(page.is_access_edit_product2_success(), "进入编辑页应成功")

    page.clean_inputs()
    page.input_product_details(name, description, price)
    page.click(page.update_button)
    soft_assert.assert_true(page.is_update_product_success(), "更新产品应成功")

    page.click(page.delete_button)
    page.click(page.cancel_delete)
    soft_assert.assert_true(page.is_return_products_main_page(), "取消删除后应返回产品主页")

    page.click(page.import_JSON_button)
    soft_assert.assert_true(page.is_access_import_JSON_page_success(), "进入导入JSON页应成功")

    # 上传功能的实际文件路径
    page.input(page.browse, str(settings_frontend.import_json_file))
    page.click(page.submit_import_button)
    soft_assert.assert_true(page.is_import_JSON_success(), "导入JSON应成功")

    soft_assert.assert_all()



