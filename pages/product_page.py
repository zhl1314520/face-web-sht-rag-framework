from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import settings_frontend


class ProductPage(BasePage):
    url = settings_frontend.config["base_url"]

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

    def open(self):
        self.driver.get(self.url)

    def is_click_create_product_button_success(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.url_contains("/new"))
            return True
        except:
            return False

    def is_view1_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/view/1")
            )
            return True
        except:
            return False

    def is_view2_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/view/2")
            )
            return True
        except:
            return False

    def is_return_products_main_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "h1"),"Products")
            )
            return True
        except:
            return False

    def is_access_edit_product2_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/edit/2")
            )
            return True
        except:
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
                EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Product successfully updated!")
            )
            return True
        except:
            return False