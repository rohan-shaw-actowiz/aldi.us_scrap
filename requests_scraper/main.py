from extract_links import get_product_list
from extract_data import get_product_details
import json

keyword = "beverages"
sku = "0000000000000296"

# get product links
def get_pl(keyword):
    data_list = get_product_list(keyword)

    with open('pl_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=2)

    print("Saved Product Links Data to pl_data.json")

    return data_list

# get product details
def get_pd(keyword, sku):
    product_details = get_product_details(keyword, sku)

    return product_details

# get product details in parallel to product links
def get_pd_with_pls(keyword):
    data_list = get_product_list(keyword)

    product_details_list = []

    for data in data_list:
        product_details = get_product_details(keyword, data['sku'])

        product_details_list.append(product_details)

    with open('pl_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=2)

    print("Saved Product Links Data to pl_data.json")

    with open('pd_data.json', 'w', encoding='utf-8') as f:
        json.dump(product_details_list, f, indent=2)

    print("Saved Product Details Data to pd_data.json")

    return product_details_list

if __name__ == "__main__":
    # get_pl(keyword)
    # get_pd(keyword, sku)
    get_pd_with_pls(keyword)