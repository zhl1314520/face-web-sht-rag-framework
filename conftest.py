import pytest, time

# from api.forgetpsd_api import ForgetPsdAPI
from core.driver_manager import DriverManager
from utils.get_token_util import get_token
# from api.user_api import UserAPI
from pages.login_page import LoginPage
from api.login_api import LoginAPI
from config.settings import settings_frontend


# from api.project_api import ProjectAPI

# ======
# 全局 fixture
# ======
@pytest.fixture(scope="session")
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

# =====================
# 全局慢速模式开关
# =====================
SLOW_MODE = True


def pause(seconds=1):
    if SLOW_MODE:
        time.sleep(seconds)

# =====================
# 管理 token
# =====================
@pytest.fixture(scope="session")
def auth_token():
    """全局 session，整个测试会话只获取一次"""
    return get_token()

# =====================
# 封装的登录 (防止别的页面操作被拦截)
# =====================
@pytest.fixture(scope="session")
def general_login(driver):
    page = LoginPage(driver)
    page.open()
    page.encapsulated_login(settings_frontend.username, settings_frontend.password)
    return page

@pytest.fixture
def login_api():
    """ 登录相关接口 """
    api = LoginAPI()
    return api


# @pytest.fixture
# def project_api():
#     api = ProjectAPI()
#     return api
