from selenium.webdriver.common.by import By
from models import GroceryLink, InputGrocery, Grocery
from utils import wait_for_element, wait_for_clickability
import time
import json

# Extracts categories name and link
def get_categories_name_and_link(driver) -> dict[str, str]:
    categories = {}

    driver.get("https://www.aldi.us/products")

    product_container = wait_for_element(driver, (By.XPATH, '//div[@class="product-category-teaser-list__content-inner product-category-teaser-list__content-inner--3-column"]'))

    for category in product_container.find_elements(By.TAG_NAME, "a"):
        categories[category.text] = category.get_attribute("href")

    return categories

# Extracts product links
def extract_product_links(driver, input_grocery: InputGrocery, limit: int = 10) -> GroceryLink:
    links = []

    driver.get("https://www.aldi.us/results?q=" + input_grocery.category)

    product_container = wait_for_element(driver, (By.XPATH, "//div[@class='product-listing-viewer__product-area']/descendant::div[@class='product-grid']"))

    for product in product_container.find_elements(By.XPATH, "//a[contains(@class, 'base-link product-tile__link')]"):
        if len(links) == limit:
            break
        links.append(product.get_attribute("href"))

    return GroceryLink(link=links)

# Extracts product details
def extract_product_details(driver, category: str, link : GroceryLink) -> Grocery:
    driver.get(link)

    product_container = wait_for_element(driver, (By.XPATH, "//div[@class='product-details']"))

    # wait_for_element(driver, (By.XPATH, "//div[@class='product-details']/img[@class='base-image zoom-on-hover__source zoom-on-hover__image']"))

    itemId = 'N/A'
    upc = 'N/A'
    productId = 'N/A'
    url = driver.current_url

    try:
        name = product_container.find_element(By.XPATH, ".//h1[@class='product-details__title']").text
    except:
        name = 'N/A'

    category = category

    try:
        image_url = product_container.find_element(By.XPATH, ".//img[@class='base-image zoom-on-hover__source zoom-on-hover__image']").get_attribute("src")
    except:
        image_url = 'N/A'
    
    storeId = 'N/A'

    storeLocation = driver.find_element(By.XPATH, ".//button[@data-test='selected-merchant-service-address']").text
    
    try:
        price = float(product_container.find_element(By.XPATH, ".//span[@class='base-price__regular']/child::span").text[1:])
    except:
        price = 0

    mrp = price

    discount = 'N/A'

    stock_availability = product_container.find_element(By.XPATH, ".//button[@data-test='product-add-cart']")

    if stock_availability.get_attribute("disabled") == None:
        availability = "In Stock"
    else:
        availability = "Out of Stock"

    keyword = name

    try:
        size = product_container.find_element(By.XPATH, ".//span[@data-test='product-details__unit-of-measurement']").text
    except:
        size = 'N/A'

    return Grocery(
    itemId=itemId,
    UPC=upc,
    productId=productId,
    URL=url,
    name=name,
    categories=category,
    image=image_url,
    storeId=storeId,
    storeLocation=storeLocation,
    price=price,
    mrp=mrp,
    discount=discount,
    availability=availability,
    keyword=keyword,
    size=size
    )
