import pytest

from core.driver_manager import DriverManager
from utils.get_token_util import get_token
from utils.logger import setup_logging
from pages.login_page import LoginPage
from api.login_api import LoginAPI
from config.settings import settings_frontend


# ======
# 初始化日志（session 最先执行）
# ======
@pytest.fixture(scope="session", autouse=True)
def init_logging():
    setup_logging()


# ======
# 浏览器驱动：class 级别，每个测试类共享，类间隔离
# ======
@pytest.fixture(scope="class")
def driver():
    driver = DriverManager.get_driver(
        browser=settings_frontend.browser,
        headless=settings_frontend.headless,
        remote_url=settings_frontend.remote_url,
    )
    driver.maximize_window()
    yield driver
    driver.delete_all_cookies()
    driver.quit()

"""
# =====================
# 全局慢速模式开关
# =====================
SLOW_MODE = True


def pause(seconds=1):
    if SLOW_MODE:
        time.sleep(seconds)
"""

# ======
# 管理 token
# ======
@pytest.fixture(scope="session")
def auth_token():
    """全局 session，整个测试会话只获取一次"""
    return get_token()


# ======
# 已登录状态：function 级别，每个用例独立登录，互不干扰
# ======
@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """提供已登录的 driver，每个用例执行前登录、执行后清除 cookie"""
    page = LoginPage(driver)
    page.open()
    page.encapsulated_login(settings_frontend.username, settings_frontend.password)
    yield driver
    driver.delete_all_cookies()


@pytest.fixture
def login_api():
    """登录相关接口"""
    return LoginAPI()
