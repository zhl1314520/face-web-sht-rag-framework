import requests
from config.settings import settings_backend


def get_token():
    session = requests.Session()
    login_response = session.post(
        settings_backend.base_url + "/login",
        data={
            "username": settings_backend.username,
            "password": settings_backend.password
        },
        allow_redirects=True
    )
    # 表单重定向认证：返回 session 对象，而非 token
    return session
