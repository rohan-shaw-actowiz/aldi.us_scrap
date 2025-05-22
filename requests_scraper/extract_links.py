import requests
from models import ProductLink

# get json of product links through keywords
def get_sku_json(query: str, storeId: str = '473-011'):
    session = requests.Session()
    headers = session.headers
    cookies = session.cookies

    params = {
        'currency': 'USD',
        'serviceType': 'pickup',
        'q': f'{query}',
        'limit': '60',
        'offset': '0',
        'getNotForSaleProducts': '0',
        'sort': 'relevance',
        'testVariant': 'A',
        'servicePoint': f'{storeId}',
    }

    response = requests.get('https://api.aldi.us/v3/product-search', params=params, headers=headers, cookies=cookies)

    res_json = response.json()

    session.close()

    return res_json

# get products links
def get_product_list(query: str, storeId: str = '473-011'):
    p_json = get_sku_json(query, storeId)

    data_list = [] 
    
    for data in p_json['data']:
        url = f"https://www.aldi.us/product/{data['urlSlugText']}-{data['sku']}"
        price = data['price']['amount']
        name = data['name']
        brandName = str(data['brandName'])
        sellingSize = data['sellingSize']
        sku = data['sku']
        urlSlugText = data['urlSlugText']
        imageUrl = data['assets'][0]['url']
        imageUrl = imageUrl.replace("{width}", "1000").replace("{slug}", urlSlugText)

        p = ProductLink(name=name, url=url, imageUrl=imageUrl, brandName=brandName, price=price, sellingSize=sellingSize, sku=sku, urlSlugText=urlSlugText, keyword=query)

        data_list.append(p.model_dump())

    return data_list

