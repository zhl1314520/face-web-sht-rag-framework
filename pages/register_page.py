from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import settings_frontend
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RegisterPage(BasePage):
    login_url = settings_frontend.base_url + "/login"
    register_url = settings_frontend.base_url + "/register"

    register_button = (By.LINK_TEXT, "Create Account")
    username_input = (By.ID, "id_username")
    password_input = (By.ID, "id_password1")
    password_confirm_input = (By.ID, "id_password2")
    register_button_create = (By.XPATH, "//button[@type='submit']")

    def open_login(self):
        self.driver.get(self.login_url)

    def click_register_button(self):
        self.click(self.register_button)

    def is_redirect_to_register(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/register")
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def input_username(self, username):
        self.input(self.username_input, username)

    def input_password(self, password):
        self.input(self.password_input, password)

    def input_password_again(self, password_confirm):
        self.input(self.password_confirm_input, password_confirm)

    def click_register_page_button(self):
        self.click(self.register_button_create)

    # 判断是否注册成功
    def is_return_to_login_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/login")
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False