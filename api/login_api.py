import allure
from core.base_api import BaseAPI
from config.settings import settings_backend

class LoginAPI(BaseAPI):

    @allure.step("调用登录接口: {username}")
    def login(self, username, password):
        url = settings_backend.base_url + "/login"

        data = {
            "username": username,
            "password": password,
        }

        # 登录接口通常会重定向到主页，所以禁止自动重定向，直接获取登录接口的响应状态码和内容
        return self.post(url, data=data, allow_redirects=False)