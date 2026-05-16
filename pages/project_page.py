from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import settings_frontend


class ProjectPage(BasePage):
    url = settings_frontend.config["base_url"]

    project_create_button = (By.XPATH, "//button[@class='navbar-toggler']")

    def open(self):
        self.driver.get(self.url)

    def is_click_create_project_button_success(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='navbar-collapse collapse show']"))
            )
            return True
        except:
            return False