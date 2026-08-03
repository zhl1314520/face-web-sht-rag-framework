"""统一 API 响应封装，避免每次手动取 result.status_code / result.json()"""


class ApiResponse:
    """将 requests.Response 封装为统一模型，提供语义化属性访问"""

    def __init__(self, response):
        self._response = response   # _response：实例（instance）属性，只要实例存在，则该属性也一定存在，这是内部属性，请尽量不要在类的外部直接访问或修改它

    @property
    def status_code(self):
        """
        由于：self._response = response 中 response 是一个对象，可以使用 self._response.status_code，例如：self 是一个”人“对象
        _response：是人的“身高”属性，同时身高属性本身也是一个对象，包含180和cm两个属性，那么 self._response.status_code 就可以表示 180 或者 cm
        但是：上面的只能对于对象有效，对于字典等类型不适合
        """
        return self._response.status_code

    @property
    def status_code_2xx(self):
        """HTTP 状态码是否为 2xx"""
        return self._response.status_code_2xx

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
        # return self     # 返回 self，使得方法可链式调用。但是不方便 debug，最好使用普通的断言，其实保留”return self“也不影响普通调用
    """
    在这段代码中，return self 的核心作用是实现 方法链式调用（Method Chaining）。

1. 什么是链式调用？
self 代表当前类的实例对象。当方法执行结束并返回 self 时，意味着你可以把多个方法用点（.）连起来连续调用，而不需要写多行临时变量。

2. 对比：有与没有 return self 的区别
❌ 如果没有 return self（默认返回 None）：
你在写测试用例时，每做一次断言就要写新的一行，或者重复调用对象：

response = api.get_user()
response.assert_status_code(200)  # 这里返回 None
# 如果还想断言别的，必须重新写一行
response.assert_json_key("name")
✅ 有 return self：
因为断言方法执行完后返回了它自己（即 response 对象本身），你可以直接在后面链式追加其他断言或方法：

# 链式调用：状态码断言通过后，紧接着验证 JSON 结构，最后获取数据
api.get_user().assert_status_code(200).assert_json_key("name")
3. 为什么在测试框架中很常见？
在接口自动化测试中（比如封装 Response 响应对象时），链式调用能让测试脚本写起来非常流畅、像写英语句子一样，极大地减少了代码冗余。
    """

    # 方法默认 2xx 都是成功，不具有普适性
    def assert_ok(self, msg=""):
        """断言 2xx"""
        if not self.status_code_2xx:
            raise AssertionError(
                msg or f"请求失败, 状态码 {self.status_code}, 响应: {self.text[:200]}"
            )
        # return self

    # 获取响应对象字符串表示 toString()
    def __repr__(self):
        return f"<ApiResponse [{self.status_code}] {self.url}>"
