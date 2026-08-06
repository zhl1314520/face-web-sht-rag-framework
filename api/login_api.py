import allure
from core.base_api import BaseAPI
from config.settings import settings_backend

class LoginAPI(BaseAPI):

    @allure.step("调用登录接口: {username}")
    def login(self, username, password):
        url = settings_backend.base_url + "/login"

        # 由于请求体参数中 Content-Type: application/x-www-from-urlencoded，那么这个属于表单提交，那么参数必须用 data 参数传递，是 return 里面的参数 data（这个） = data
        # 若果请求体参数中 Content-Type: application/json，那么参数必须用 json，属于json提交
        data = {    # 这个 data 只是变量名，不一定非得是 data，可以是 payload，data，json。。。
            "username": username,
            "password": password,
        }

        # 登录接口通常会重定向到主页，所以禁止自动重定向，直接获取登录接口的响应状态码和内容
        # 若是 json 提交，则用 json=json，data 是表单提交，data=data
        return self.post(url, data=data, allow_redirects=False)