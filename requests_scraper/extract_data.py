import requests
from models import ProductLink, Product

# get json of product page
def get_product_json(sku: str, storeId: str = '473-011'):
    session = requests.Session()
    headers = session.headers
    cookies = session.cookies

    params = {
        'servicePoint': f'{storeId}',
        'serviceType': 'pickup',
    }

    response = requests.get(f'https://api.aldi.us/v2/products/{sku}', params=params, headers=headers, cookies=cookies)

    res_json = response.json()

    session.close()

    return res_json

# get store address for product
def get_store_address(storeId: str = '473-011'):
    session = requests.Session()
    headers = session.headers
    cookies = session.cookies

    params = {
        'include': 'merchant-addresses',
    }

    response = requests.get(f'https://api.aldi.us/v1/merchants/{storeId}', params=params, headers=headers, cookies=cookies)

    res_json = response.json()

    session.close()

    return res_json

# get product details
def get_product_details(keyword: str, sku: str, storeId: str = '473-011'):
    p_json = get_product_json(sku, storeId)
    a_json = get_store_address(storeId)

    data = p_json['data']
    name = data['name']
    url = f"https://www.aldi.us/product/{data['urlSlugText']}-{data['sku']}"
    imageUrl = data['assets'][0]['url']
    image = imageUrl.replace("{width}", "1000").replace("{slug}", data['urlSlugText'])
    price = data['price']['amount']
    size = data['sellingSize']
    availability = 'In stock' if data["stockInformationAvailable"] == None else "Out of stock"
    categories = [i['name'] for i in data['categories']]
    keyword = keyword

    address_block = a_json['included'][0]['attributes']['addresses'][0]
    storeLocation = f"{address_block['zipCode']}, {address_block['city']}"

    p = Product(name=name, url=url, image=image, price=price, mrp=price, size=size, availability=availability, categories=categories, keyword=keyword, storeId=storeId, storeLocation=storeLocation)

    return p.model_dump()

