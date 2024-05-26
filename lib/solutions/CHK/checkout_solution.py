from collections import Counter, OrderedDict


def offer_details(offer_description):
    details = [word.strip() for word in offer_description.split('for')]
    return extract_leading_number(details[0]), int(details[1])


def process_get_one_free_offers(items, one_free_offers):
    items_to_deduct = {}

    for item, qty in items.items():
        if item in one_free_offers:
            # check if item meets quantity threshold
            offer_description = one_free_offers[item]
            offer_description_details = [word.strip() for word in offer_description.replace('free', '').split('get one')]
            offer_qty = extract_leading_number(offer_description_details[0])
            free_item = offer_description_details[1]

            # handle operation where get one free offer pertains to same item/product
            if free_item == item:
                item_set = offer_qty + 1
                items_to_pay_for = (qty // item_set) * offer_qty + (qty % item_set)
                items_to_deduct[free_item] = qty - items_to_pay_for
                continue

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
    arranged_parsed_offers = OrderedDict(sorted(parsed_offers.items(), key=lambda item: int(item[0]), reverse=True))

    return arranged_parsed_offers


def extract_leading_number(s):
    number_str = ''

    for char in s:
        if char.isdigit():
            number_str += char
        else:
            break

    # convert extracted number string to int
    if number_str:
        return int(number_str)
    else:
        return None


def process_group_discount(grp_disc_products, grp_disc_price, discount_threshold, basket_items, price_table):
    # separate the group discount products into their own basket.
    grp_discount_basket_items = OrderedDict((k, basket_items.pop(k)) for k in grp_disc_products if k in basket_items)

    # Calculate product item prices in group discount basket
    # First calculate the total quantity of promotional items
    promo_items_qty = sum(grp_discount_basket_items.get(item, 0) for item in grp_disc_products)

    # Calculate the promotional discount to be given
    promo_discount = 0
    if promo_items_qty >= discount_threshold:
        promo_groups = promo_items_qty // discount_threshold
        promo_discount = promo_groups * grp_disc_price

    # quantity of promo items that are outside the discount quantity threshold
    non_discount_promo_items_qty = promo_items_qty % discount_threshold

    # Arrange grp_discount_basket_items according to their prices in ascending order
    # then, calculate the amount to pay on items that don't meet the discount threshold,
    # prioritising the cheapest products. That is [(item, qty, price)]. E.g. [('X',2,17),('S',2,20),...]
    grp_discount_basket_items_list = [(item, qty, price_table[item]) for item, qty in grp_discount_basket_items.items()]
    sorted_grp_discount_basket_items_list = sorted(grp_discount_basket_items_list, key=lambda item: item[2])

    non_discount_items_price = 0
    for item in sorted_grp_discount_basket_items_list:
        if non_discount_promo_items_qty <= item[1]:
            non_discount_items_price += non_discount_promo_items_qty * item[2]
            break
        else:
            non_discount_items_price += item[1] * item[2]
            non_discount_promo_items_qty = non_discount_promo_items_qty - item[1]

    total_price_for_group_discount_items = promo_discount + non_discount_items_price

    return basket_items, total_price_for_group_discount_items


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_table = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15,
        'E': 40,
        'F': 10,
        'G': 20,
        'H': 10,
        'I': 35,
        'J': 60,
        'K': 70,
        'L': 90,
        'M': 15,
        'N': 40,
        'O': 10,
        'P': 50,
        'Q': 30,
        'R': 50,
        'S': 20,
        'T': 20,
        'U': 40,
        'V': 50,
        'W': 20,
        'X': 17,
        'Y': 20,
        'Z': 21
    }

    offers = {
        'A': '3A for 130, 5A for 200',
        'B': '2B for 45',
        'C': '',
        'D': '',
        'E': '',
        'F': '',
        'G': '',
        'H': '5H for 45, 10H for 80',
        'I': '',
        'J': '',
        'K': '2K for 120',
        'L': '',
        'M': '',
        'N': '',
        'O': '',
        'P': '5P for 200',
        'Q': '3Q for 80',
        'R': '',
        'S': '',
        'T': '',
        'U': '',
        'V': '2V for 90, 3V for 130',
        'W': '',
        'X': '',
        'Y': '',
        'Z': ''
    }

    get_one_free_offers = {
        'E': '2E get one B free',
        'F': '2F get one F free',
        'N': '3N get one M free',
        'R': '3R get one Q free',
        'U': '3U get one U free',
    }

    group_discount_products = ['S', 'T', 'X', 'Y', 'Z']
    group_discount_price = 45
    group_discount_threshold = 3

    total = 0

    if isinstance(skus, str) and len(skus) > 0:
        items = Counter(skus)

        # process get one free offers
        items = process_get_one_free_offers(items, get_one_free_offers)

        # process group discount items
        items, grp_discount_total = process_group_discount(group_discount_products,
                                                           group_discount_price,
                                                           group_discount_threshold,
                                                           items,
                                                           price_table)
        total += grp_discount_total

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

