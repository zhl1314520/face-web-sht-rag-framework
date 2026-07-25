import logging
import requests

logger = logging.getLogger(__name__)


class BaseAPI:
    def __init__(self):
        self.session = requests.Session()   # session 对象管理：复用 TCP 连接（更快）、自动带 cookie（登录态）、可以统一加 headers（token）

    def _log_request(self, method, url, **kwargs):  # **kwargs: 允许传入任意参数
        logger.info("%s %s | 参数: %s", method, url, kwargs)

    def _log_response(self, result):
        logger.info("响应: %s | %s", result.status_code, result.text)

    def get(self, url, **kwargs):
        self._log_request("GET", url, **kwargs)
        result = self.session.get(url, **kwargs)
        self._log_response(result)
        return result

    def post(self, url, **kwargs):
        self._log_request("POST", url, **kwargs)
        result = self.session.post(url, **kwargs)
        self._log_response(result)
        return result

    def put(self, url, **kwargs):
        self._log_request("PUT", url, **kwargs)
        result = self.session.put(url, **kwargs)
        self._log_response(result)
        return result

    def delete(self, url, **kwargs):
        self._log_request("DELETE", url, **kwargs)
        result = self.session.delete(url, **kwargs)
        self._log_response(result)
        return result