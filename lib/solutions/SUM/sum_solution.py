# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x, y):
    # validate parameters
    if not (0 <= x <= 100 and 0 <= y <= 100):
        raise ValueError("Both parameters must be integers between 0 and 100")

    return x + y


