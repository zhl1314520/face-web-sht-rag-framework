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
    logout_button = (By.XPATH,  "//a[contains(@href,'logout')]")

    def open(self):
        self.driver.get(self.url)

    def input_username(self, username):
        self.input(self.username_input, username)

    def input_password(self, password):
        self.input(self.password_input, password)

    def click_login_button(self):
        self.click(self.login_button)

    def is_login_successful(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "alert-success")
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def logout(self):
        try:
            self.click(self.logout_button)
            # 等待回到登录页或确认退出成功
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            pass  # 如果已经退出或找不到退出按钮，忽略

    # 封装的 login
    def encapsulated_login(self, username, password):
        self.open()
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()