import logging
import requests
from core.api_response import ApiResponse

logger = logging.getLogger(__name__)


class BaseAPI:
    def __init__(self):
        self.session = requests.Session()  # session 对象管理：复用 TCP 连接（更快）、自动带 cookie（登录态）、可以统一加 headers（token）

    def _log_request(self, method, url, **kwargs):  # **kwargs: 允许传入任意参数
        logger.info("%s %s | 参数: %s", method, url, kwargs)

    def _log_response(self, resp):
        logger.info("响应: %s | %s", resp.status_code, resp.text[:500])

    def _request(self, method, url, **kwargs):
        """统一请求入口，返回 ApiResponse"""
        self._log_request(method, url, **kwargs)
        resp = getattr(self.session, method)(url, **kwargs) # getattr: 动态调用，一个（）负责”找方法“，一个负责”执行方法“
        """
        等价于：
        # 1. 第一步：用 getattr 拿到方法本身（注意这里没有括号，只是获取函数对象）
        http_method_func = getattr(self.session, method)

        # 2. 第二步：在拿到方法后面直接加括号，传入参数并执行它 ，**kwargs：关键字参数解包
        resp = http_method_func(url, **kwargs)
        
        
        假设：
        client._request("post", "https://api.com/users", json={"name": "Alice"})
        """
        self._log_response(resp)
        return ApiResponse(resp)

    def get(self, url, **kwargs):
        return self._request("get", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("post", url, **kwargs)

    def put(self, url, **kwargs):
        return self._request("put", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("delete", url, **kwargs)
