import logging
import requests
from core.api_response import ApiResponse

logger = logging.getLogger(__name__)


class BaseAPI:
    def __init__(self):
        self.session = requests.Session()

    def _log_request(self, method, url, **kwargs):
        logger.info("%s %s | 参数: %s", method, url, kwargs)

    def _log_response(self, resp):
        logger.info("响应: %s | %s", resp.status_code, resp.text[:500])

    def _request(self, method, url, **kwargs):
        """统一请求入口，返回 ApiResponse"""
        self._log_request(method, url, **kwargs)
        resp = getattr(self.session, method)(url, **kwargs)
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
