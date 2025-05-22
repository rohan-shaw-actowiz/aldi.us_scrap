from scraper.extract_links import get_categories_name_and_link, extract_product_links, extract_product_details
from utils import get_driver, close_driver, json_to_excel
from models import InputGrocery, Grocery
import json

# Extracts categories name and link
def getCategories():
    categories = get_categories_name_and_link(driver)

    with open("categories.json", "w") as f:
        json.dump(categories, f)

# Extracts product links
def getProductLinks(limit : int = 12):
    product_links_json = {}

    for category in categories.keys():
        if category == "Featured":
            continue
        product_links_json[category] = []

        input_grocery = InputGrocery(category=category)
        links = extract_product_links(driver,input_grocery, limit=limit)

        for link in links.link:
            product_links_json[category].append(link)

    with open("product_links.json", "w") as f:
        json.dump(product_links_json, f)

# Extracts groceries
def getGroceries(product_links_json, categories_limit: int = None):
    groceries = {}

    for category in list(product_links_json.keys())[:categories_limit if categories_limit != None else len(product_links_json.keys())]:
        groceries[category] = []

        for link in product_links_json[category]:
            groceries[category].append(extract_product_details(driver, category, link).dict())

    with open("groceries.json", "w") as f:
        json.dump(groceries, f)

if __name__ == "__main__":
    driver = get_driver()
    try: 
        # getCategories()

        with open("categories.json", "r") as f:
            categories = json.load(f)

        # getProductLinks()

        with open("product_links.json", "r") as f:
            product_links_json = json.load(f)

        # getGroceries(product_links_json)

        with open("groceries.json", "r") as f:
            groceries = json.load(f)

        json_to_excel(groceries, "groceries.xlsx")
        
    finally:
        close_driver(driver)