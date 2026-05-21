import os

# 跑所有用例
def run_all():
    os.system("pytest -v")

# 跑指定目录
def run_dir(dir):
    os.system("pytest " + dir + " -v")

# 跑指定文件
def run_file(file):
    os.system("pytest " + file + " -v")

# 跑指定用例
def run_case(file, name):
    os.system("pytest " + file + "::" + name + " -v" + " -s")

if __name__ == "__main__":
    """ API """


    """ UI """
    # run_case("tests/ui/test_login.py", "test_login")

    # run_case("tests/ui/test_register.py", "test_register")

    # run_case("tests/ui/test_product.py", "test_product_create_button")

    run_case("tests/ui/test_product.py", "test_product2_function_button")