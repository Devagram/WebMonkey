import time
import difflib
import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from google.adk.tools import FunctionTool
from .metrics import metrics_tracker
import undetected_chromedriver as uc


_driver = None
_driver_profile_dir = None

def get_driver():
    global _driver, _driver_profile_dir
    if _driver is None:
        chrome_profile_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "selenium_profile"))
        options = uc.ChromeOptions()
        options.add_argument(f'--user-data-dir={chrome_profile_path}')
        options.add_argument("--start-maximized")
        _driver = uc.Chrome(options=options)
    return _driver

def close_driver():
    global _driver, _driver_profile_dir
    if _driver:
        _driver.quit()
        _driver = None
    # Remove the temporary profile directory
    if _driver_profile_dir and os.path.exists(_driver_profile_dir):
        shutil.rmtree(_driver_profile_dir, ignore_errors=True)
        _driver_profile_dir = None

def reset_driver_session():
    close_driver()
    _ = get_driver()

def search_product(product_name: str) -> dict:
    reset_driver_session()
    driver = get_driver()
    try:
        driver.get("https://www.bunnings.com.au")
        time.sleep(5)

        input_box = driver.find_element(By.ID, "custom-css-outlined-input")
        input_box.clear()
        input_box.send_keys(product_name)
        input_box.send_keys(Keys.ENTER)

        max_wait = 10
        for _ in range(max_wait):
            time.sleep(1)
            if "search/products" in driver.current_url and "q=" in driver.current_url:
                break

        return {"status": "success", "url": driver.current_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}
search_product_tool = FunctionTool(func=search_product)


def list_products(product_name: str) -> dict:
    driver = get_driver()
    products = []
    start_time = time.time()
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, "article.search-product-tile")
        if not cards:
            end_time = time.time()
            metrics_tracker.record("list_products", "error", start_time, end_time, "No product cards found.")
            return {"status": "error", "message": "No product cards found."}

        for card in cards:
            try:
                name_elem = card.find_element(By.CSS_SELECTOR, "p[data-locator^='search-product-tile-title-']")
                name = name_elem.text.strip()

                ratio = difflib.SequenceMatcher(None, product_name.lower(), name.lower()).ratio()
                if ratio >= 0.5:
                    img = card.find_element(By.CSS_SELECTOR, "img.product-tile-image").get_attribute("src")
                    url = card.find_element(By.CSS_SELECTOR, "a.sc-e0f7877-1").get_attribute("href")
                    products.append({"name": name, "image": img, "url": url, "match_score": ratio})
            except Exception:
                continue

        products.sort(key=lambda x: x["match_score"], reverse=True)

        end_time = time.time()
        if products:
            metrics_tracker.record("list_products", "success", start_time, end_time)
            return {"status": "success", "products": products}
        else:
            metrics_tracker.record("list_products", "error", start_time, end_time, f"No close matches for '{product_name}'")
            return {"status": "error", "message": f"No close matches for '{product_name}'"}
    except Exception as e:
        end_time = time.time()
        metrics_tracker.record("list_products", "error", start_time, end_time, str(e))
        return {"status": "error", "message": str(e)}
list_products_tool = FunctionTool(func=list_products)


def add_to_cart_by_url(product_url: str) -> dict:
    driver = get_driver()
    start_time = time.time()
    try:
        driver.get(product_url)
        time.sleep(3)
        add_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Add to cart button']")
        add_btn.click()
        time.sleep(2)
        end_time = time.time()
        metrics_tracker.record("add_to_cart_by_url", "success", start_time, end_time)
        return {"status": "success", "message": f"Product added to cart: {product_url}"}
    except Exception as e:
        end_time = time.time()
        metrics_tracker.record("add_to_cart_by_url", "error", start_time, end_time, str(e))
        return {"status": "error", "message": str(e), "url": product_url}

add_to_cart_tool = FunctionTool(func=add_to_cart_by_url)

def proceed_to_checkout() -> dict:
    driver = get_driver()
    try:

        driver.get("https://www.bunnings.com.au/cart")
        time.sleep(8)
        try:
            checkout_btn = driver.find_element(By.ID, "customerDetailsButton")
            checkout_btn.click()
            time.sleep(5)
            return {"status": "success", "message": "Proceeded to checkout."}
        except Exception as e:
            return {"status": "error", "message": f"Checkout button not found: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

proceed_to_checkout_tool = FunctionTool(func=proceed_to_checkout)
