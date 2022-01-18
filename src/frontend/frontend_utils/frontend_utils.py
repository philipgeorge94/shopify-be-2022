def get_yn(prompt):
    response = input(prompt).lower()
    if response == 'yes' or response == 'y':
        return True
    else:
        return False


def refresh_prod_lookups(prods_data):
    print(str(len(prods_data)) + ' products in database')
    prod_ids = {}
    for prod in prods_data:
        prod_ids[prod['prod_id']] = prod['_id']
    return prod_ids

def print_prod_data(prods_data):
    print()
    print(str(len(prods_data)) + ' product(s) retrieved. Printing...')
    print()
    for prod in prods_data:
        prod_str = []
        for key, value in prod.items():
            prod_str.append(key + " = " + value)
        print(" | ".join(prod_str[1:]))
    return
