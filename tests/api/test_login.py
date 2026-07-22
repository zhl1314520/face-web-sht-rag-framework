import pytest

@pytest.mark.parametrize("username,password,expected_status", [
    ("admin", "zxcvbnm", 302),
    ("17263937422@163.com", "", 200),
    ("", "123456", 200),
])
def test_login(login_api, username, password, expected_status):
    result = login_api.login(username, password)
    assert result.status_code == expected_status