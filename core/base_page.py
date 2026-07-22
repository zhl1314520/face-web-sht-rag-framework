from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import settings_frontend


class BasePage:
    # 构造函数（初始化方法）：创建 BasePage 对象自动执行
    def __init__(self, driver, timeout=None):
        self.driver = driver
        self.timeout = timeout or settings_frontend.timeout
        self.wait = WebDriverWait(driver, self.timeout)

    # 封装等待方法：查找单个元素
    def find(self, locator):    # locator ：一个元组 (定位策略, 定位值) ，例如 (By.ID, "email")
        # presence_of_element_located: Selenium 的预期等待条件，等待元素出现在 DOM 中
        return self.wait.until(EC.presence_of_element_located(locator))

    def finds(self, locator):
        self.wait.until(EC.presence_of_all_elements_located(locator))   # 等待元素加载
        return self.driver.find_elements(*locator)

    # 封装等待方法：等待元素出现后再点击
    def click(self, locator):
        self.find(locator).click()

    # 封装等待方法：等待元素出现后再输入
    def input(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def accept_alert(self):
        """处理浏览器弹窗"""
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert.accept()
            return True
        except (TimeoutException, NoSuchElementException):
            return False