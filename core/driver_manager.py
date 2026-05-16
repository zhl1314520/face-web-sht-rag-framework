from selenium import webdriver


class DriverManager:

    # 代理 ChromeOptions
    ChromeOptions = webdriver.ChromeOptions

    # 代理 Chrome
    @staticmethod
    def Chrome(options=None):
        return webdriver.Chrome(options=options)