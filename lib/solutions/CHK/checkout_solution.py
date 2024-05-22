from collections import Counter


def offer_details(offer_description):
    details = [word.strip() for word in offer_description.split('for')]
    return int(details[0][0]), int(details[1])


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_table = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15
    }

    offers = {
        'A': '3A for 130',
        'B': '2B for 45',
        'C': '',
        'D': ''
    }

    total = 0

    if isinstance(skus, str) and len(skus) > 0:
        items = Counter(skus)

        for item, qty in items.items():
            try:
                item_special_offers = offers[item]
                if not bool(item_special_offers):
                    # if no special offer on item, calc price in relation to qty
                    total += price_table[item] * qty
                else:
                    # calc pricing of item based off special offer
                    item_offer_qty, item_offer_price = offer_details(item_special_offers)

                    if qty >= item_offer_qty:
                        # check the item quantity meets minimum requirements for special offer
                        qty_of_item_covered_by_offer = qty // item_offer_qty
                        qty_of_item_not_covered_by_offer = qty % item_offer_qty

                        price_covered_by_offer = qty_of_item_covered_by_offer * item_offer_price
                        price_not_covered_by_offer = qty_of_item_not_covered_by_offer * price_table[item]

                        item_total = price_covered_by_offer + price_not_covered_by_offer
                        total += item_total
                    else:
                        # item not eligible for offer pricing, calculate price as normal
                        total += price_table[item] * qty
            except KeyError as e:
                total = -1
                break

    return total

