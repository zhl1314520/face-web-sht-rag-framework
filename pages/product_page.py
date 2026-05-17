from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import settings_frontend


class ProductPage(BasePage):
    url = settings_frontend.config["base_url"]

    product_view = (By.XPATH, "//a[contains(@href, '/view/1')]")
    view1_products = (By.LINK_TEXT, "Products")
    view1_edit = (By.XPATH, "//a[contains(@href, '/edit/1')]")
    product_name_input = (By.ID, "id_name")
    product_description_input = (By.ID, "id_description")
    product_price_input = (By.ID, "id_price")

    def open(self):
        self.driver.get(self.url)

    def is_view_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/view/1")
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

    def input_product_details(self, name, description, price):
        self.input(self.product_name_input, name)
        self.input(self.product_description_input, description)
        self.input(self.product_price_input, price)