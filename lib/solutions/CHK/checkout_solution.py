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

    total = 0

    if isinstance(skus, str):
        items = Counter(skus)

        for item, qty in items:
            total += price_table[item] * qty

    return total






