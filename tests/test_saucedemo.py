import os
import sys
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import get_driver, login

URL = 'https://www.saucedemo.com/'
USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login(driver):
        login(driver)

        # Verificar que el login fue exitoso comprobando que estamos en la página de productos
        WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
            )

        # Verifica que estamos en el inventario
        assert '/inventory.html' in driver.current_url, "No se redirigió a la página de inventario después del login"

        # Verifica que exista el elemento del título y que su texto sea 'Swag Labs'
        titulo = driver.find_element(By.CLASS_NAME, "app_logo")
        assert titulo, "No se encontró el elemento con clase 'app_logo'"
        assert titulo.text == "Swag Labs", f"Texto inesperado en logo: se esperaba 'Swag Labs' pero se obtuvo '{titulo.text}'"

        # Verifica título de sección
        seccion = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
        assert seccion == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion}'"

        print('Login completado correctamente y se ingresó a la página de inventario.')

def test_catalogo(driver):
    login(driver)

    # Verifica título de sección
    titulo = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
    assert titulo == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{titulo}'"
