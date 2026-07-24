import logging

from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import settings_frontend
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    url = settings_frontend.base_url

    product_create_button = (By.LINK_TEXT, "New Product")
    product_view1 = (By.XPATH, "//a[contains(@href, '/view/1')]")
    product_view2 = (By.XPATH, "//a[contains(@href, '/view/2')]")
    view1_products = (By.LINK_TEXT, "Products")
    view1_edit = (By.XPATH, "//a[contains(@href, '/edit/1')]")
    view2_edit = (By.XPATH, "//a[contains(@href, '/edit/2')]")
    product_name_input = (By.ID, "id_name")
    product_description_input = (By.ID, "id_description")
    product_price_input = (By.ID, "id_price")
    update_button = (By.XPATH, "//button[contains(@type, 'submit')]")
    delete_button = (By.XPATH, "//a[contains(@href, '/delete/2')]")
    cancel_delete = (By.LINK_TEXT, "Cancel")
    import_JSON_button = (By.LINK_TEXT, "Import JSON")
    browse = (By.ID, "jsonFile")
    submit_import_button = (By.XPATH, "//button[contains(@type, 'submit')]")

    def open(self):
        self.driver.get(self.url)

    def is_click_create_product_button_success(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.url_contains("/new"))
            return True
        except TimeoutException as e:
            logger.warning(f"点击创建产品按钮后未跳转到 /new: {e}")
            return False

    def is_view1_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/view/1")
            )
            return True
        except TimeoutException as e:
            logger.warning(f"未成功跳转到 /view/1: {e}")
            return False

    def is_view2_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/view/2")
            )
            return True
        except TimeoutException as e:
            logger.warning(f"未成功跳转到 /view/2: {e}")
            return False

    def is_return_products_main_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "h1"),"Products")
            )
            return True
        except TimeoutException as e:
            logger.warning(f"未返回产品主页: {e}")
            return False

    def is_access_edit_product2_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/edit/2")
            )
            return True
        except TimeoutException as e:
            logger.warning(f"未成功跳转到 /edit/2: {e}")
            return False

    def clean_inputs(self):
        self.find(self.product_name_input).clear()
        self.find(self.product_description_input).clear()
        self.find(self.product_price_input).clear()

    def input_product_details(self, name, description, price):
        self.input(self.product_name_input, name)
        self.input(self.product_description_input, description)
        self.input(self.product_price_input, price)

    def is_update_product_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"),
                                                 "Product successfully updated!")
            )
            return True
        except TimeoutException as e:
            logger.warning(f"产品更新失败或未出现成功提示: {e}")
            return False

    def is_access_import_JSON_page_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "importJsonModalLabel"))
            )
            return True
        except TimeoutException as e:
            logger.warning(f"导入 JSON 弹窗未出现: {e}")
            return False

    def is_import_JSON_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"),
                                                 "Successfully imported 1 product(s).")
            )
            return True
        except TimeoutException as e:
            logger.warning(f"JSON 导入失败或未出现成功提示: {e}")
            return False