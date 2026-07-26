"""统一 API 响应封装，避免每次手动取 result.status_code / result.json()"""


class ApiResponse:
    """将 requests.Response 封装为统一模型，提供语义化属性访问"""

    def __init__(self, response):
        self._response = response

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def ok(self):
        """HTTP 状态码是否为 2xx"""
        return self._response.ok

    @property
    def text(self):
        return self._response.text

    @property
    def json(self):
        """解析响应体为 dict/list"""
        try:
            return self._response.json()
        except ValueError:
            return {}

    @property
    def headers(self):
        return self._response.headers

    @property
    def elapsed(self):
        """请求耗时（秒）"""
        return self._response.elapsed.total_seconds()

    @property
    def url(self):
        return self._response.url

    def assert_status_code(self, expected, msg=""):
        """断言状态码，失败时抛出带上下文信息的 AssertionError"""
        if self.status_code != expected:
            raise AssertionError(
                msg or f"状态码期望 {expected}, 实际 {self.status_code}, 响应: {self.text[:200]}"
            )
        return self

    def assert_ok(self, msg=""):
        """断言 2xx"""
        if not self.ok:
            raise AssertionError(
                msg or f"请求失败, 状态码 {self.status_code}, 响应: {self.text[:200]}"
            )
        return self

    def __repr__(self):
        return f"<ApiResponse [{self.status_code}] {self.url}>"
