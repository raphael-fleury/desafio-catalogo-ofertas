import re
from products.models import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_driver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception:
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        except Exception:
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")
            return webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

def collect_data():
    url = "https://www.mercadolivre.com.br"
    search_term = "Computador Gamer i7 16gb ssd 1tb"

    driver = get_driver()
    driver.get(url)

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "as_word"))
    )
    search_box.send_keys(search_term)
    search_box.submit()

    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[@class="ui-search-layout__item"]'))
    )

    for product in products:
        try:
            current_price_selector = './/div[contains(@class, "poly-price__current")]'
            price_amount_selector = '//span[contains(@class, "andes-money-amount__fraction")]'
            original_price_selector = './/s[contains(@class, "andes-money-amount--previous")]'
            discount_selector = './/span[contains(@class, "andes-money-amount__discount")]'

            name = product.find_element(By.XPATH, './/a').text
            price = product.find_element(
                By.XPATH, f'{current_price_selector}{price_amount_selector}'
            ).text

            img_element = product.find_element(By.XPATH, './/img[contains(@class, "poly-component__picture")]')
            image = img_element.get_attribute("data-src") \
                or img_element.get_attribute("srcset") \
                or img_element.get_attribute("src")

            original_price_element = product.find_elements(
                By.XPATH, f'{original_price_selector}{price_amount_selector}'
            )
            original_price = original_price_element[0].text if original_price_element else price

            discount_element = product.find_elements(By.XPATH, discount_selector)
            discount_text = discount_element[0].text if discount_element else "0%"

            installment_options = product.find_element(By.XPATH, './/span[contains(@class, "poly-price__installments")]').text
            link = product.find_element(By.XPATH, './/h3//a').get_attribute("href")
            delivery_type = "Full" if "FULL" in product.text else "Normal"
            free_shipping = "frete grátis" in product.text.lower() or "Chegará grátis" in product.text

            Product.objects.create(
                name=name,
                image=image,
                price=float(price.replace('.', '').replace(',', '.')),
                link=link,
                delivery_type=delivery_type,
                free_shipping=free_shipping,
                original_price=float(original_price.replace('.', '').replace(',', '.')),
                discount_percentage=int(re.sub(r"\D", "", discount_text)),
                installment_options=installment_options
            )
        except Exception as e:
            print(f"Error on creating product: {e}")

    driver.quit()