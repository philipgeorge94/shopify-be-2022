def get_yn(prompt):
    response = input(prompt).lower()
    if response == 'yes' or response == 'y':
        return True
    else:
        return False


def refresh_prod_lookups(self, prods_data):
    print(str(len(prods_data)) + ' products in database')
    prod_ids = {}
    for prod in prods_data:
        prod_ids[prod['prod_id']] = prod['_id']
    return prod_ids
