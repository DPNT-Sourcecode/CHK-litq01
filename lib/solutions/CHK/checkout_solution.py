from collections import Counter


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_table = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15
    }

    if not isinstance(skus, str):
        raise ValueError("parameter must be a string")

    items = Counter(skus)

    total = 0

    for item, qty in items:
        total += price_table[item] * qty

    return total





