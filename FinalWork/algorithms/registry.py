"""@register 装饰器 —— 自动将算法函数注册到全局 ALGORITHMS 字典"""

ALGORITHMS: dict[str, dict[str, callable]] = {}


def register(tab_name: str, algo_name: str):
    """装饰器：自动将算法函数注册到全局 ALGORITHMS 字典

    用法:
        @register("灰度变换", "线性变换")
        def linear_transform(image, alpha=1.0, beta=0):
            ...
    """
    def decorator(func):
        if tab_name not in ALGORITHMS:
            ALGORITHMS[tab_name] = {}
        ALGORITHMS[tab_name][algo_name] = func
        return func
    return decorator
