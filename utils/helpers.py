import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL = 'https://www.saucedemo.com/'
USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

def get_driver():
    options = Options()
    options.add_argument('--start-maximized') # Ventana grande
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5) # Espera implícita
    return driver

def login(driver):
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

def captura_de_pantalla(driver, caso):
    # Guarda una captura de pantalla con tiempo y nombre de test.
    os.makedirs("reports", exist_ok=True)
    tiempo = datetime.now().strftime("%d-%m-%Y %S-%M-%H")
    archivo = f"reports/{caso}_{tiempo}.png"
    driver.save_screenshot(archivo)
    print(f"Screenshot guardado en: {archivo}")