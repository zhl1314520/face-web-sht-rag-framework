import logging

logger = logging.getLogger(__name__)


class SoftAssert:
    """软断言：收集所有失败，最后统一抛出，避免第一个断言失败就中断"""

    def __init__(self):
        # 解释 _errors 没有定义直接可以使用：Python 的实例属性（instance attribute）不需要提前声明，第一次赋值时就会自动创建
        # 只要你有一个对象实例 self，就可以动态创建实例属性。__init__ 只是最常见、最推荐的位置
        # 只能在类方法中使用这样形式（不定义直接用），普通非类内函数不可以这样
        self._errors = []

    # 当断言 true 失败时，记录错误信息到 _errors 列表中，并打印警告日志
    def assert_true(self, actual, msg=""):
        if not actual:
            error_msg = msg or f"期望 True, 实际 {actual}"
            self._errors.append(error_msg)
            logger.warning("断言失败: %s", error_msg)

    def assert_false(self, actual, msg=""):
        if actual:
            error_msg = msg or f"期望 False, 实际 {actual}"
            self._errors.append(error_msg)
            logger.warning("断言失败: %s", error_msg)

    def assert_equal(self, actual, expected, msg=""):
        if actual != expected:
            error_msg = msg or f"期望 {expected}, 实际 {actual}"
            self._errors.append(error_msg)
            logger.warning("断言失败: %s", error_msg)

    def assert_not_equal(self, actual, expected, msg=""):
        if actual == expected:
            error_msg = msg or f"期望不等于 {expected}, 实际 {actual}"
            self._errors.append(error_msg)
            logger.warning("断言失败: %s", error_msg)

    def assert_all(self):
        """断言全部收集完毕后调用，有失败则统一抛出"""
        if self._errors:
            error_summary = "\n".join(f"  {i+1}. {e}" for i, e in enumerate(self._errors))
            raise AssertionError(f"共 {len(self._errors)} 个断言失败:\n{error_summary}")
