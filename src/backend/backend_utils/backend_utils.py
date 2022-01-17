def get_prod_id_list(all_prods):
    prod_ids = {}
    print("in get_prod_id_list function")
    for prod in all_prods:
        prod_ids[prod['prod_id']] = prod['_id']
    return prod_ids
