import logging
import pytest
import allure
from core.driver_manager import DriverManager
from utils.get_token_util import get_token
from utils.logger import setup_logging
from pages.login_page import LoginPage
from api.login_api import LoginAPI
from config.settings import settings_frontend
from api.register_api import RegisterAPI

"""
问题：
    为什么都调用了底层的 logging 还要自己写个 logger.py 工具函数
解答：
    1. logging 是 Python 标准库，默认没有格式（输出是裸文本）、级别是 WARNING，而（INFO、DEBUG会被丢弃），只输出到控制台，没有输出到文件
    2. 工具函数 logger.py 所有 logger 自动带格式、同时输出到控制台和文件、级别受控

logging.getLogger()          ← 根 logger（所有 logger 的父节点）
  ├── setLevel(INFO)         ← 设置全局级别
  ├── addHandler(控制台)     ← 加控制台输出 + 格式
  └── addHandler(文件)       ← 加文件输出 + 格式
"""
logger = logging.getLogger(__name__)    # 创建 logger 实例


# ======
# 初始化日志（session 最先执行，范围最大）  scope ：session > module > class > function
# 无论是哪个测试类、哪个测试函数，都会先执行这个 fixture
# ======
@pytest.fixture(scope="session", autouse=True)  # scope="session", autouse=True：整个测试会话只执行一次，最先执行，自动执行
def init_logging():
    """仅仅是初始化配置，没有创建logger实例，要想使用log，必须创建实例"""
    setup_logging()


# ======
# 浏览器驱动：class 级别，每个测试类共享，不同测试类隔离
# ======
@pytest.fixture(scope="class")
def driver():
    # get_driver 是静态方法，DriverManager 是类
    # @staticmethod 标记的方法是不需要创建对象调用该方法，直接使用类即可调用
    driver = DriverManager.get_driver(
        browser=settings_frontend.browser,
        headless=settings_frontend.headless,
        remote_url=settings_frontend.remote_url,
    )
    driver.maximize_window()
    """
    分为 3 个阶段
    1. 准备阶段：执行 yield driver 之前的代码，即准备资源（setup）
    2. 测试阶段：yield driver：把 driver 交给测试函数使用，然后暂停这里，直到测试阶段结束
    3. 清理阶段：即 teardown 阶段，测试阶段结束后执行 yield driver 后面的代码，释放资源
    """
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
    return LoginAPI()   # 返回 LoginAPI 对象

@pytest.fixture
def register_api():
    """注册相关接口"""
    return RegisterAPI()


# ======
# 数据清理：用例执行后清理测试产生的数据，不是所有的数据都要清理，只有那些会影响后续测试的数据（或指定的数据）才需要清理，所以没有设计为”autouse = true“
# ======
# @pytest.fixture(scope="function")   # 函数级：每执行一个测试函数，就创建一个新的 cleanup
# def cleanup():
#     """注册清理回调，用例结束后自动执行。用法: cleanup(delete_user, user_id)"""
#     callbacks = []  # 保存测试结束后需要执行的清理动作数据
#
#     # 注册清理任务
#     """
#     如：cleanup(delete_user, 1)
#     那么callbacks = [
#         (delete_user, (1,), {})
#     ]
#     """
#     def add_cleanup(callback, *args, **kwargs):
#         callbacks.append((callback, args, kwargs))  # 测试结束后调用 delete_user(1)
#
#     yield add_cleanup  # 核心：进入 fixture -> callbacks[] -> yield register -> 测试函数执行 -> 测试结束 -> 继续执行 yield 下面的代码
#
#     for callback, args, kwargs in reversed(callbacks):  # reversed：倒叙执行清理，避免还有未完成的进程
#         try:
#             callback(*args, **kwargs)   # *args: (1,), **kwargs: {} 解包
#         except Exception as e:
#             logger.warning("清理回调执行失败: %s", e)


# ======
# 失败自动截图
# 监听每个测试用例的执行结果，如果测试失败，自动截图，并把截图挂到 Allure 报告中
# ======
@pytest.hookimpl(hookwrapper=True)  # hookwrapper 是一个 hook，wrapper 器，底层逻辑：1. 执行完测试用例后，继续处理测试结果，2. 处理测试结果时，继续处理截图逻辑
def pytest_runtest_makereport(item, call):  # pytest 每执行一个测试，会生成一个测试报告
    """
    借 pytest 已经写好的生命周期和状态数据（report.when 等）
    借 pytest 提供的 Hook 拦截点（pytest_runtest_makereport）
    实现你自己的业务：当判断出测试失败（report.failed）且正处于核心执行阶段（report.when == "call"）时，
    自动调用 Selenium/Playwright 的 driver 进行截图并塞进 Allure 报告里

    1. pytest_runtest_makereport 是谁写的？
        不是 Python 标准库写的，而是 pytest 框架内置的 Hook 规范（插件接口）。
        pytest 在运行测试的各个阶段（准备、执行、清理）会主动发出这些钩子信号。
        你写的这个函数（带 @pytest.hookimpl 装饰器）是向 pytest 注册的一个自定义插件/回调，
        告诉 pytest：“当执行到生成报告这个步骤时，顺便执行我的这段逻辑”。

    2. report.when、report.failed 等属性是哪来的？
        这些都是 pytest 在底层运行测试时，自动计算并封装好的现成属性（属于 TestReport 对象）：
        report.when：表示测试的当前阶段，由 pytest 自动区分：
        "setup"：前置准备阶段（如 @pytest.fixture 初始化）
        "call"：测试用例正文执行阶段
        "teardown"：后置清理阶段
        report.failed / report.passed：布尔值，pytest 自动判断当前阶段是成功还是失败。
        report.duration(持续时间)：float 类型，pytest 自动记录该阶段消耗的时间。
        report.nodeid：字符串，pytest 自动生成的测试用例唯一标识（包含模块名、类名、函数名等）
        report.longreprtext：字符串，pytest 自动生成的失败信息（包含断言失败的堆栈、异常类型、异常信息等）

    前半段（yield 之前）：在 Pytest 官方的“生成报告”核心逻辑执行之前运行
    yield 暂停：交出控制权，让 Pytest 去执行它原本的“生成报告”底层代码
    后半段（yield 之后）：当 Pytest 的底层代码执行完毕后，控制权交还给你的函数，代码从 yield 的下一行继续运行

    为什么这里必须用 yield？
        因为“截图”这个动作，必须发生在测试报告已经生成之后。如果在测试报告还没生成时就去截图，
        或者你不知道测试到底成功还是失败，你就无法判断 report.failed 是否为 True。yield 巧妙地实现了：先让 Pytest 
        把报告跑出来 $\rightarrow$ 你的代码通过 outcome = yield 拿到这个报告 $\rightarrow$ 检查发现
        失败了 $\rightarrow$ 顺便拍个照存起来
    """
    execute_results = yield # 先让 pytest 执行完测试用例，生成报告，然后将结果报告交给 execute_results
    report = execute_results.get_result()

    if report.when == "call" and report.failed:
        # 失败用例写入日志
        logger.error("用例失败: %s\n%s", item.nodeid, report.longreprtext)
        driver = None  # 初始化 driver 变量
        # 从 fixture 中获取 driver
        if "driver" in item.funcargs:  # item.funcargs 是一个字典，存储了当前测试函数的所有 fixture 参数及其值
            driver = item.funcargs["driver"]
        elif "logged_in_driver" in item.funcargs:   # logged_in_driver 在上文中是个函数（提供登录过的 driver）
            driver = item.funcargs["logged_in_driver"]

        if driver:
            try:
                screenshot_dir = settings_frontend.screenshot_dir
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                filename = f"{item.name}_{report.when}.png"
                path = screenshot_dir / filename
                driver.save_screenshot(str(path))
                logger.info("测试失败截图已保存: %s", path)

                # 附加到 Allure 报告
                allure.attach.file(str(path), name=filename, attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                logger.warning("截图失败: %s", e)
