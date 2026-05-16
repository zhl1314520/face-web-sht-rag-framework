from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


""" UI 基类"""
class BasePage:     # 所有继承 BasePage 的都带有显式等待

    # 大量使用 self：每个页面类实例都有自己的 wait 对象（login_page, dashboard_page 等）

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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