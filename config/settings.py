import yaml

class SettingsBackend:
    # 后端配置
    def __init__(self, env="dev-backend"):
        with open("config/env.yaml", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.config = data[env]

settings_backend = SettingsBackend()

class SettingsFrontend:
    # 前端配置
    def __init__(self, env="dev-frontend"):
        with open("config/env.yaml", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.config = data[env]

settings_frontend = SettingsFrontend()