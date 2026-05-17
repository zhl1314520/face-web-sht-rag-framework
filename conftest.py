import pytest, time

# from api.forgetpsd_api import ForgetPsdAPI
from core.driver_manager import DriverManager
# from api.auth_api import AuthAPI
# from utils.get_token_util import get_token
# from api.user_api import UserAPI
from pages.login_page import LoginPage
# from api.project_api import ProjectAPI

# ======
# 全局 fixture
# ======
@pytest.fixture(scope="session")
def driver():
    options = DriverManager.ChromeOptions()
    options.page_load_strategy = "eager"
    driver = DriverManager.Chrome(options=options)
    driver.maximize_window()  # 浏览器窗口最大化
    yield driver
    driver.delete_all_cookies()  # 清理 cookies（仅仅是test_login使用）
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
# @pytest.fixture(scope="session")
# def auth_token():
#     """全局 token，整个测试会话只获取一次"""
#     return get_token()

# =====================
# 封装的登录 (防止别的页面操作被拦截)
# =====================
@pytest.fixture(scope="session")
def general_login(driver):
    page = LoginPage(driver)
    page.open()
    page.encapsulated_login("admin", "zxcvbnm")
    return page
#
#
# # 用户认证相关接口（带有 token）
# @pytest.fixture
# def auth_api_with_token(auth_token):
#     """带 token 的 auth_api"""
#     api = AuthAPI()
#     api.token = auth_token  # 将 token 绑定到实例
#     return api
#
# # 用户管理相关接口
# @pytest.fixture
# def user_api(auth_token):
#     api = UserAPI()
#     api.token = auth_token
#     return api
#
#

# # 项目管理相关接口
# @pytest.fixture
# def project_api():
#     api = ProjectAPI()
#     return api
