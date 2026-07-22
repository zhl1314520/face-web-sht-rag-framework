import os
from pathlib import Path
import yaml


class Settings:
    """统一配置管理，支持多环境切换，同一环境只创建一次对象"""

    # 类变量
    _instances = {}

    def __init__(self, env="dev"):  # 构造函数（初始化方法）：创建 Settings 对象自动执行
        # __file__： 当前文件的路径，如 D:\...\config\settings.py，Path(__file__) 将路径转为 Path 对象
        # 变成了：WindowsPath('D:/.../config/settings.py')
        # Path(__file__).parent：获取当前文件的父目录，即 config 目录
        # / 运算符重载：Path 对象可以使用 / 拼接路径
        config_path = Path(__file__).parent / "env.yaml"
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)  # safe_load 只能读取数据，不可以执行恶意代码

        self.config = data.get(env, {})     # env 配置
        self.accounts = data.get("accounts", {})  # accounts 配置
        self.common = data.get("common", {})# common 配置

    @property       # 作用：调用函数时不需要加括号，直接用属性的方式访问，如 settings.base_url，而不是 settings.base_url()
    def base_url(self):
        return self.config.get("base_url", "")

    @property
    def username(self):
        # 优先从环境变量读取，便于 CI/CD 注入；否则读取 accounts.admin 配置, 如果都没有则返回空字符串
        # TEST_USERNAME: 环境变量名
        return os.environ.get("TEST_USERNAME", self.accounts.get("admin", {}).get("username", ""))

    @property
    def password(self):
        return os.environ.get("TEST_PASSWORD", self.accounts.get("admin", {}).get("password", ""))

    def get_account(self, role="admin"):
        """按角色获取账号信息，如 settings.get_account('developer')"""
        account = self.accounts.get(role, {})
        return {
            "username": os.environ.get("TEST_USERNAME", account.get("username", "")),
            "password": os.environ.get("TEST_PASSWORD", account.get("password", "")),
        }

    @property
    def timeout(self):
        # 如果 env.yaml 中没有配置 timeout，则使用 common 中的默认值 10
        return self.common.get("timeout", 10)

    @property
    def test_data_dir(self):
        project_root = Path(__file__).parent.parent # 获取项目根目录，可以一直 .parent...
        return project_root / self.common.get("test_data_dir", "test_data")

    @property
    def import_json_file(self):
        return self.test_data_dir / self.common.get("import_json_file", "products.json")


# 按环境缓存配置对象
def get_settings(env="dev-backend"):    # 定义参数，设置默认值为 dev-backend
    """单例模式：获取配置单例，同一环境只加载一次"""
    if env not in Settings._instances:
        Settings._instances[env] = Settings(env)       # 结果： _instances 里面存了 dev-backend 对象地址
    return Settings._instances[env]


# 预创建常用配置实例
settings_backend = get_settings("dev-backend")
settings_frontend = get_settings("dev-frontend")