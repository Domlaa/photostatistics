import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()   # 更精确的计时
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] 执行耗时: {end - start:.4f} 秒")
        return result
    return wrapper
