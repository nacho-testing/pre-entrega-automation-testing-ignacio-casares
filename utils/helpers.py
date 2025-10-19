from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    options.add_argument('--start-maximized') # Ventana grande
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5) # Espera implícita
    return driver