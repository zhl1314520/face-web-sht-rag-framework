from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import settings_frontend
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage(BasePage):
    url = settings_frontend.config["base_url"] + "/login"

    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    login_button = (By.CLASS_NAME, "btn")   # 不要选择全部的 btn，可能会有多个

    def open(self):
        self.driver.get(self.url)

    def input_username(self, username):
        self.input(self.username_input, username)

    def input_password(self, password):
        self.input(self.password_input, password)

    def click_login_button(self):
        self.click(self.login_button)

    def clear_inputs(self):
        self.find(self.username_input).clear()
        self.find(self.password_input).clear()

    def is_login_successful(self):
        try:
            self.find((By.CLASS_NAME, "alert-success"))
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def return_login_page(self):
        self.driver.back()