import logging
import requests


""" 日志 """
logger = logging.getLogger(__name__)

""" 接口封装 """

class BaseAPI:
    def __init__(self):
        self.session = requests.Session()   # session 对象管理：复用 TCP 连接（更快）、自动带 cookie（登录态）、可以统一加 headers（token）

    def get(self, url, **kwargs):   # **kwargs：允许传入任意参数
        logger.info(f"GET URL: {url}")
        logger.info(f"参数: {kwargs}")

        result = self.session.get(url, **kwargs)

        logger.info(f"状态码: {result.status_code}")
        logger.info(f"响应: {result.text}")

        return result

    def post(self, url, **kwargs):
        logger.info(f"请求 URL: {url}")
        logger.info(f"请求参数: {kwargs}")

        result = self.session.post(url, **kwargs)

        logger.info(f"响应状态码: {result.status_code}")
        logger.info(f"响应内容: {result.text}")

        return result

    def put(self, url, **kwargs):
        logger.info(f"请求 URL: {url}")
        logger.info(f"请求参数: {kwargs}")

        result = self.session.put(url, **kwargs)

        logger.info(f"响应状态码: {result.status_code}")
        logger.info(f"响应内容: {result.text}")

        return result

    def delete(self, url, **kwargs):
        logger.info(f"请求 URL: {url}")
        logger.info(f"请求参数: {kwargs}")

        result = self.session.delete(url, **kwargs)

        logger.info(f"响应状态码: {result.status_code}")
        logger.info(f"响应内容: {result.text}")

        return result