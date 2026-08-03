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
    """浏览器驱动管理：多浏览器、headless、保存密码弹窗、远程 WebDriver、驱动自动管理"""

    @staticmethod       # 这里可以不使用静态方法，但使用静态方法可以避免实例化 DriverManager 对象，直接通过类名调用方法
    # 静态方法：详见 my-files/测开/@staticmethod.md
    # 本函数获取 chrome 选项
    def _create_chrome_options(headless=False):     # _开头的函数：内部调用函数（模块内部私有函数），但是可以被外部调用，只是不建议，这是约定
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")  # 新版 Chrome headless 模式，旧版是 --headless
        options.add_argument("--disable-gpu")   # 关闭 GPU 加速，现在的新版 Chrome 已经不需要这个参数了，但为了兼容旧版，还是加上
        options.add_argument("--no-sandbox")    # 在 Linux docker CI 中，Chrome 需要加上这个参数，否则会报错，win 一般没事
        options.add_argument("--disable-dev-shm-usage") # Linux docker 共享内存不足时，Chrome 会崩溃，需要加上这个参数
        options.add_argument("--start-maximized") # 启动时最大化窗口，CI建议固定窗口大小
        options.page_load_strategy = "eager" # 页面加载策略，normal：所有图片、js、css全部加载完才继续，eager：DOM加载完直接继续，适合自动化

        # 禁用弹出密码保存弹窗
        preferences = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False    # 禁止弹出密码泄露
        }
        options.add_experimental_option(
            "prefs",
            preferences
        )
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
        service = ChromeService(ChromeDriverManager().install())    # 创建 ChromeService 对象，ChromeDriverManager()：自动下载 Chrome 驱动
        options = DriverManager._create_chrome_options(headless)
        logger.info("启动 Chrome 浏览器, headless=%s", headless)
        # 创建 Chrome 对象，service：即 driver，options：即浏览器选项
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
        """连接远程 WebDriver（Selenium Grid / Docker）
            简单理解：A 电脑写代码，B 电脑跑用例
                    B电脑启动 Selenium Server：java -jar selenium-server.jar standalone  ---> 192.168.1.20:4444
                    那么：remote_url = "http://192.168.1.20:4444"
        """
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
        """统一入口：根据配置创建浏览器对象"""
        if remote_url:
            return DriverManager.create_remote(remote_url, browser, headless)

        drivers = {
            "chrome": DriverManager.create_chrome,
            "firefox": DriverManager.create_firefox,
            "edge": DriverManager.create_edge,
        }
        create_browser_obj = drivers.get(browser)
        if create_browser_obj is None:
            logger.warning("不支持的浏览器类型: %s, 回退到 Chrome", browser)
            create_browser_obj = DriverManager.create_chrome
        return create_browser_obj(headless=headless)
