import allure
from core.base_api import BaseAPI
from config.settings import settings_backend

class RegisterAPI(BaseAPI):

    @allure.step("调用注册接口: {username}")
    def register(self, username, password1, password2):
        url = settings_backend.base_url + "/register"

        data = {
            "username": username,
            "password1": password1,
            "password2": password2,
        }

        return self.post(url, data=data, allow_redirects=False, need_csrf=True)