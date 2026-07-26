from pages.product_page import ProductPage
import pytest
from config.settings import settings_frontend
from utils.data_loader import load_test_data

""" UI 项目模块 """

product_data = load_test_data("ui_product.json")
# 参数列表
product_params = []
for data in product_data:
    product_params.append(tuple(data.values()))

create_data = [{"expected_success": True}]  # 目前只有一组数据，看起来没有必要，但为了后续扩展，保留了参数化的形式

@pytest.mark.parametrize("expected_success", [d["expected_success"] for d in create_data]) # 当 create_data 里面有 2 组以上的数据时，就非常有必要使用[]来保存，如[true, False], 一次性批量执行参数化
def test_product_create_button(logged_in_driver, expected_success):
    page = ProductPage(logged_in_driver)
    page.open()
    page.click(page.product_create_button)

    assert page.is_click_create_product_button_success() == expected_success, "点击创建产品按钮后应成功进入创建页"


def test_product_view(logged_in_driver):
    """测试查看产品详情"""
    page = ProductPage(logged_in_driver)
    page.open()
    page.click(page.product_view2)

    assert page.is_view2_success(), "查看产品详情应成功"


@pytest.mark.parametrize("name, description, price, expected_success", product_params)
def test_product_edit(logged_in_driver, name, description, price, expected_success):
    """测试编辑产品"""
    page = ProductPage(logged_in_driver)
    page.open()
    page.click(page.product_view2)
    assert page.is_view2_success(), "查看产品详情应成功"

    page.click(page.view2_edit)
    assert page.is_access_edit_product2_success(), "进入编辑页应成功"

    page.clean_inputs()
    page.input_product_details(name, description, price)
    page.click(page.update_button)
    assert page.is_update_product_success() == expected_success, "更新产品应成功"


def test_product_cancel_delete(logged_in_driver):
    """测试取消删除产品"""
    page = ProductPage(logged_in_driver)
    page.open()
    page.click(page.product_view2)

    page.click(page.delete_button)
    page.click(page.cancel_delete)
    assert page.is_return_products_main_page(), "取消删除后应返回产品主页"


def test_product_import_json(logged_in_driver):
    """测试导入 JSON"""
    page = ProductPage(logged_in_driver)
    page.open()
    page.click(page.import_JSON_button)
    assert page.is_access_import_JSON_page_success(), "进入导入JSON页应成功"

    # 上传功能的实际文件路径
    page.input(page.browse, str(settings_frontend.import_json_file))
    page.click(page.submit_import_button)
    assert page.is_import_JSON_success(), "导入JSON应成功"



