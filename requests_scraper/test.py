from extract_links import *
from models import *

j = get_sku_json("game day")

for d in j['data']:
    url = f"https://www.aldi.us/product/{d['urlSlugText']}-{d['sku']}"
    price = d['price']['amount']
    imageUrl = d['assets'][0]['url']
    name = d['name']
    brandName = str(d['brandName'])
    sellingSize = d['sellingSize']
    sku = d['sku']
    urlSlugText = d['urlSlugText']

    # img url : https://dm.cms.aldi.cx/is/image/prod1amer/product/jpg/scaleWidth/{width}/f930ac7f-53e6-47df-9cc5-255635f661d5/{slug}

    imageUrl = imageUrl.replace("{width}", "1000").replace("{slug}", urlSlugText)

    p = ProductLink(name=name, url=url, imageUrl=imageUrl, brandName=brandName, price=price, sellingSize=sellingSize, sku=sku, urlSlugText=urlSlugText, keyword="game day")

    print(p)