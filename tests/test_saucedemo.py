import os
import sys
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import get_driver

URL = 'https://www.saucedemo.com/'
USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login(driver):
    driver.get(URL)
    
    # Verifica título de la página
    assert driver.title == 'Swag Labs'

    print('Se ingresó correctamente a la página {} con el título esperado: {}', URL, 'Swag Labs')

    # Espera a que se cargue el formulario de login
    WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user-name"))
            )

    # Verifica y completa los campos de login y hace clic en el botón de iniciar sesión, verificando que cada elemento exista
    assert driver.find_element(By.ID, "user-name"), "No se encontró el campo de usuario"
    driver.find_element(By.ID, "user-name").send_keys(USERNAME)
    assert driver.find_element(By.ID, "password"), "No se encontró el campo de contraseña"
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    assert driver.find_element(By.ID, "login-button"), "No se encontró el botón de login"
    driver.find_element(By.ID, "login-button").click()

    print("Se completaron correctamente los campos de login y se hizo clic en el botón.")