import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import settings_frontend

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, timeout=None):
        self.driver = driver
        self.timeout = timeout or settings_frontend.timeout
        self.wait = WebDriverWait(driver, self.timeout)

    # 封装等待方法：查找单个元素
    def find(self, locator):    # locator：元组（定位策略，定位值），如：（By.id，"email"）
        logger.debug("查找元素: %s", locator)   # locator：元组, 所以 log 里面显示的是两个数据
        # presence_of_element_located: 等待元素出现在 DOM 中，但不一定可见
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_element(*locator)

    def finds(self, locator):
        logger.debug("查找多个元素: %s", locator)
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        logger.info("点击元素: %s", locator)
        self.find(locator).click()

    def input(self, locator, text):
        logger.info("输入文本: %s -> %s", locator, text)
        element = self.find(locator)
        element.clear()     # 输入前清空
        element.send_keys(text)     # 输入文本

    def accept_alert(self):
        """处理浏览器弹窗"""
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert.accept()
            logger.info("已接受弹窗")
            return True
        except (TimeoutException, NoSuchElementException):
            logger.debug("无弹窗需要处理")
            return False