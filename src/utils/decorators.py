from functools import wraps
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver(func):
    @wraps(func)
    def wrapper(url, *args, **kwargs):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        # options.binary_location = "/usr/bin/google-chrome"
        # service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            result = func(url, driver, *args, **kwargs)
        finally:
            driver.quit()
        return result
    return wrapper

def validate_data(required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            for key in required_keys:
                if data.get(key) is None:
                    raise ValueError(f'Missing required data: {key}')
            return data
        return wrapper
    return decorator

def handle_http_request(func):
    @wraps(func)
    def wrapper(url, *args, **kwargs):
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f'Error en la solicitud: {response.status_code}')
        soup = BeautifulSoup(response.content, 'html.parser')
        return func(url, soup, *args, **kwargs)
    return wrapper