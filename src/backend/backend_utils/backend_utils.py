import pandas as pd
import os
import datetime


def get_prod_id_list(all_prods):
    prod_ids = {}
    print("in get_prod_id_list function")
    for prod in all_prods:
        prod_ids[prod['prod_id']] = prod['_id']
    return prod_ids


def export_to_csv(prods_data):
    df = pd.DataFrame.from_dict(prods_data)
    print(df)
    for (columnName, columnData) in df.iteritems():
        print(f'Column Name :*{columnName}*')
        print('Column Contents : ', columnData.values)
    df = df.drop(["_id"], axis=1)
    print(df)
    df.to_csv((fname := f'{os.getcwd()}/server_file_storage/Products_{datetime.datetime.now()}.csv'), index=False)
    return fname
