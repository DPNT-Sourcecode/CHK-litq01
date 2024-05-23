from collections import Counter, OrderedDict


def offer_details(offer_description):
    details = [word.strip() for word in offer_description.split('for')]
    return int(details[0][0]), int(details[1])


def process_get_one_free_offers(items, one_free_offers):
    items_to_deduct = {}

    for item, qty in items.items():
        if item in one_free_offers:
            # check if item meets quantity threshold
            offer_description = one_free_offers[item]
            offer_description_details = [word.strip() for word in offer_description.replace('free', '').split('get one')]
            offer_qty = int(offer_description_details[0][0])
            free_item = offer_description_details[1]

            if qty >= offer_qty:
                free_item_qty = qty // offer_qty
            else:
                free_item_qty = 0

            items_to_deduct[free_item] = free_item_qty

    # check if item to deduct is already in the checkout basket, if not remove
    free_items_not_in_basket = [free_item for free_item in items_to_deduct.keys() if free_item not in items]

    for item in free_items_not_in_basket:
        items_to_deduct.pop(item)

    # remove quantity of free items from items to calc
    for free_item, free_item_qty in items_to_deduct.items():
        if items[free_item] <= free_item_qty:
            items[free_item] = 0
        else:
            items[free_item] = items[free_item] - free_item_qty

    return items


def parse_compound_offer(offer_string):
    # separate offers
    offers = offer_string.split(',')

    # parse offers
    parsed_offers = OrderedDict()
    for offer in offers:
        item_offer_qty, item_offer_price = offer_details(offer)
        parsed_offers[str(item_offer_qty)] = item_offer_price

    # arrange the offers in descending order of qty
    arranged_parsed_offers = OrderedDict(sorted(parsed_offers.items(), key=lambda item: item[0], reverse=True))

    return arranged_parsed_offers


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_table = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15,
        'E': 40,
        'F': 10
    }

    offers = {
        'A': '3A for 130, 5A for 200',
        'B': '2B for 45',
        'C': '',
        'D': '',
        'E': '',
        'F': ''
    }

    get_one_free_offers = {
        'E': '2E get one B free',
        'F': '2F get one F free'
    }

    total = 0

    if isinstance(skus, str) and len(skus) > 0:
        items = Counter(skus)

        # process get one free offers
        items = process_get_one_free_offers(items, get_one_free_offers)

        for item, qty in items.items():
            try:
                item_special_offers = offers[item]
                if not bool(item_special_offers):
                    # if no special offer on item, calc price in relation to qty
                    total += price_table[item] * qty
                else:
                    # check if offer is a compound special offer by checking for a "," in offer description,
                    # and calculate prices accordingly.
                    if ',' in item_special_offers:
                        compound_offer_details = parse_compound_offer(item_special_offers)
                        item_total = 0

                        # calculate items that fall under special offers
                        for offer_qty, offer_price in compound_offer_details.items():
                            if qty >= int(offer_qty):
                                item_total += (qty // int(offer_qty)) * offer_price
                                qty = qty % int(offer_qty)

                        # calculate items not covered by special offers
                        item_total += price_table[item] * qty

                        total += item_total
                        continue

                    # calc pricing of item based off simple special offer
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
