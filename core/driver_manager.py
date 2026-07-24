import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


class DriverManager:
    """浏览器驱动管理：多浏览器、headless、远程 WebDriver、驱动自动管理"""

    @staticmethod       # 这里可以不使用静态方法，但使用静态方法可以避免实例化 DriverManager 对象，直接通过类名调用方法
    def _create_chrome_options(headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.page_load_strategy = "eager"
        return options

    @staticmethod
    def _create_firefox_options(headless=False):
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return options

    @staticmethod
    def _create_edge_options(headless=False):
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.page_load_strategy = "eager"
        return options

    @staticmethod
    def create_chrome(headless=False):
        service = ChromeService(ChromeDriverManager().install())
        options = DriverManager._create_chrome_options(headless)
        logger.info("启动 Chrome 浏览器, headless=%s", headless)
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def create_firefox(headless=False):
        service = FirefoxService(GeckoDriverManager().install())
        options = DriverManager._create_firefox_options(headless)
        logger.info("启动 Firefox 浏览器, headless=%s", headless)
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def create_edge(headless=False):
        service = EdgeService(EdgeChromiumDriverManager().install())
        options = DriverManager._create_edge_options(headless)
        logger.info("启动 Edge 浏览器, headless=%s", headless)
        return webdriver.Edge(service=service, options=options)

    @staticmethod
    def create_remote(remote_url, browser="chrome", headless=False):
        """连接远程 WebDriver（Selenium Grid / Docker）"""
        options_map = {
            "chrome": DriverManager._create_chrome_options,
            "firefox": DriverManager._create_firefox_options,
            "edge": DriverManager._create_edge_options,
        }
        options_fn = options_map.get(browser, DriverManager._create_chrome_options)
        options = options_fn(headless)
        logger.info("连接远程 WebDriver: %s, browser=%s", remote_url, browser)
        return webdriver.Remote(command_executor=remote_url, options=options)

    @staticmethod
    def get_driver(browser="chrome", headless=False, remote_url=""):
        """统一入口：根据配置创建浏览器实例"""
        if remote_url:
            return DriverManager.create_remote(remote_url, browser, headless)

        drivers = {
            "chrome": DriverManager.create_chrome,
            "firefox": DriverManager.create_firefox,
            "edge": DriverManager.create_edge,
        }
        create_fn = drivers.get(browser)
        if create_fn is None:
            logger.warning("不支持的浏览器类型: %s, 回退到 Chrome", browser)
            create_fn = DriverManager.create_chrome
        return create_fn(headless=headless)
