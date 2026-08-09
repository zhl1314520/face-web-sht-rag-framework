import requests
from config.settings import settings_backend


def get_login_session():
    """返回带登录态的 session 对象"""
    session = requests.Session()
    session.post(
        settings_backend.base_url + "/login",
        data={
            "username": settings_backend.username,
            "password": settings_backend.password
        },
        allow_redirects=True
    )
    # 表单重定向认证：返回 session 对象，而非 token
    return session
