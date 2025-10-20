import os
import sys
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import get_driver, login, captura_de_pantalla

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login(driver):
    try:
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

    except Exception as e:
        captura_de_pantalla(driver, 'test_login')
        raise e
    
def test_catalogo(driver):
    try:
        login(driver)

        # Verifica título de sección
        titulo = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
        assert titulo == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{titulo}'"

        verifica_menu(driver)
        verifica_filtro(driver)
        verifica_carrito(driver)

        # Confirma que aparece al menos un div.inventory_item
        productos = driver.find_elements(By.CSS_SELECTOR, "div.inventory_item")
        assert len(productos) > 0, "No se encontraron productos en el catálogo"

        # Verifica que cada producto tenga nombre y precio visibles
        for producto in productos:
            assert producto.find_element(By.CLASS_NAME, "inventory_item_name"), "Producto sin nombre"
            assert producto.find_element(By.CLASS_NAME, "inventory_item_price"), "Producto sin precio"

        # Muestra en consola el nombre y precio del primer producto
        primer_producto = productos[0]
        nombre_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

        print(f"Nombre: {nombre_del_producto}")
        print(f"Precio: {precio_del_producto}")

    except Exception as e:
        captura_de_pantalla(driver, 'test_catalogo')
        raise e

def test_carrito(driver):
    try:
        login(driver)

        # Verifica título de sección
        print("Verificando el título de la sección")
        titulo = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
        assert titulo == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{titulo}'"

        # Confirma que aparece al menos un div.inventory_item
        print("Buscando productos en el catálogo")
        productos = driver.find_elements(By.CSS_SELECTOR, "div.inventory_item")
        assert len(productos) > 0, "No se encontraron productos en el catálogo"

        primer_producto = productos[0]
        
        # Verifica que existan el nombre y el precio del primer producto
        print("Verificando que el primer producto tenga nombre y precio...")

        assert primer_producto.find_element(By.CLASS_NAME, "inventory_item_name"), "Producto sin nombre"
        assert primer_producto.find_element(By.CLASS_NAME, "inventory_item_price"), "Producto sin precio"

        nombre_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

        print(f"Primer producto: Nombre: {nombre_del_producto}, Precio: {precio_del_producto}")

        # Verifica que exista el botón "Add to cart" en el primer producto
        print("Verificando que exista el botón 'Add to cart' en el primer producto")
        boton_agregar = primer_producto.find_element(By.XPATH, ".//button[text()='Add to cart']")
        assert boton_agregar, "No se encontró el botón 'Add to cart' en el primer producto"

        # Haz clic en "Add to cart" del primer producto
        print("Haciendo clic en el botón 'Add to cart'")
        boton_agregar = primer_producto.find_element(By.XPATH, ".//button[text()='Add to cart']")
        boton_agregar.click()

        # Verifica que el contador del carrito muestre 1
        print("Verificando que el contador del carrito muestre 1")
        carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        assert carrito, "No se encontró el icono del carrito"

        # Espera explícita para que aparezca el contador del carrito
        print("Esperando que aparezca el contador del carrito")
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )

        contador = carrito.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(contador) > 0, "No se encontró el contador del carrito después de agregar el producto"

        # Ingresa al carrito
        print("Ingresando al carrito")
        carrito.click()
        
        # Espera explícita a que cargue la página del carrito
        WebDriverWait(driver, 8).until(
            EC.url_contains("/cart.html")
        )
        assert '/cart.html' in driver.current_url, "No se redireccionó correctamente a la página del carrito"
    
        # Verifica que exista la lista de productos del carrito
        print("Verificando que exista la lista de productos en el carrito")
        la_lista_de_los_productos_del_carrito = driver.find_elements(By.CLASS_NAME, "cart_list")
        assert len(la_lista_de_los_productos_del_carrito) > 0, "No se encontró la lista de productos en el carrito"

        productos_del_carrito = la_lista_de_los_productos_del_carrito[0].find_elements(By.CLASS_NAME, "cart_item")
        assert len(productos_del_carrito) == 1, f"Se esperaba 1 producto en el carrito, pero se encontraron {len(productos_del_carrito)}"
        
        # Verificar que el producto añadido esté en la lista
        print("Verificando que el producto añadido sea el correcto")
        el_producto_esperado = productos_del_carrito[0]

        nombre_en_carrito = el_producto_esperado.find_element(By.CLASS_NAME, 'inventory_item_name')
        assert nombre_en_carrito, "No se encontró el nombre del producto en el carrito"
        assert nombre_en_carrito.text == nombre_del_producto, (
            f"Nombre inesperado en el carrito: se esperaba {nombre_del_producto} pero se obtuvo {nombre_en_carrito.text}"
        )

        precio_en_carrito = el_producto_esperado.find_element(By.CLASS_NAME, 'inventory_item_price')
        assert precio_en_carrito, "No se encontró el precio del producto en el carrito"
        assert precio_en_carrito.text == precio_del_producto, (
            f"Precio inesperado en el carrito: se esperaba {precio_del_producto} pero se obtuvo {precio_en_carrito.text}"
        )

        print("El producto en el carrito coincide con el producto añadido.")

    except Exception as e:
        captura_de_pantalla(driver, 'test_carrito')
        raise e
    
def test_carrito(driver):
    login(driver)

    # Verifica título de sección
    print("Verificando el título de la sección")
    titulo = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
    assert titulo == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{titulo}'"

    # Confirma que aparece al menos un div.inventory_item
    print("Buscando productos en el catálogo")
    productos = driver.find_elements(By.CSS_SELECTOR, "div.inventory_item")
    assert len(productos) > 0, "No se encontraron productos en el catálogo"

    primer_producto = productos[0]
        
    # Verifica que existan el nombre y el precio del primer producto
    print("Verificando que el primer producto tenga nombre y precio...")

    assert primer_producto.find_element(By.CLASS_NAME, "inventory_item_name"), "Producto sin nombre"
    assert primer_producto.find_element(By.CLASS_NAME, "inventory_item_price"), "Producto sin precio"

    nombre_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio_del_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

    print(f"Primer producto: Nombre: {nombre_del_producto}, Precio: {precio_del_producto}")

    # Verifica que exista el botón "Add to cart" en el primer producto
    print("Verificando que exista el botón 'Add to cart' en el primer producto")
    boton_agregar = primer_producto.find_element(By.XPATH, ".//button[text()='Add to cart']")
    assert boton_agregar, "No se encontró el botón 'Add to cart' en el primer producto"

    # Haz clic en "Add to cart" del primer producto
    print("Haciendo clic en el botón 'Add to cart'")
    boton_agregar = primer_producto.find_element(By.XPATH, ".//button[text()='Add to cart']")
    boton_agregar.click()

    # Verifica que el contador del carrito muestre 1
    print("Verificando que el contador del carrito muestre 1")
    carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    assert carrito, "No se encontró el icono del carrito"

    # Espera explícita para que aparezca el contador del carrito
    print("Esperando que aparezca el contador del carrito")
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    contador = carrito.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(contador) > 0, "No se encontró el contador del carrito después de agregar el producto"

    # Ingresa al carrito
    print("Ingresando al carrito")
    carrito.click()
        
    # Espera explícita a que cargue la página del carrito
    WebDriverWait(driver, 8).until(
        EC.url_contains("/cart.html")
    )
    assert '/cart.html' in driver.current_url, "No se redireccionó correctamente a la página del carrito"
    
    # Verifica que exista la lista de productos del carrito
    print("Verificando que exista la lista de productos en el carrito")
    la_lista_de_los_productos_del_carrito = driver.find_elements(By.CLASS_NAME, "cart_list")
    assert len(la_lista_de_los_productos_del_carrito) > 0, "No se encontró la lista de productos en el carrito"

    productos_del_carrito = la_lista_de_los_productos_del_carrito[0].find_elements(By.CLASS_NAME, "cart_item")
    assert len(productos_del_carrito) == 1, f"Se esperaba 1 producto en el carrito, pero se encontraron {len(productos_del_carrito)}"
        
    # Verificar que el producto añadido esté en la lista
    print("Verificando que el producto añadido sea el correcto")
    el_producto_esperado = productos_del_carrito[0]

    nombre_en_carrito = el_producto_esperado.find_element(By.CLASS_NAME, 'inventory_item_name')
    assert nombre_en_carrito, "No se encontró el nombre del producto en el carrito"
    assert nombre_en_carrito.text == nombre_del_producto, (
        f"Nombre inesperado en el carrito: se esperaba {nombre_del_producto} pero se obtuvo {nombre_en_carrito.text}"
    )

    precio_en_carrito = el_producto_esperado.find_element(By.CLASS_NAME, 'inventory_item_price')
    assert precio_en_carrito, "No se encontró el precio del producto en el carrito"
    assert precio_en_carrito.text == precio_del_producto, (
        f"Precio inesperado en el carrito: se esperaba {precio_del_producto} pero se obtuvo {precio_en_carrito.text}"
    )

    print("El producto en el carrito coincide con el producto añadido.")

def verifica_menu(driver):
    # Verifica que exista el botón de menú lateral antes de hacer clic
    menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
    assert menu_button, "No se encontró el botón con clase 'react-burger-menu-btn'"
    print("Botón de menú encontrado.")

    # Abre el menú lateral haciendo clic en el botón de menú (hamburguesa)
    print("Haciendo clic en el botón de menú lateral")
    menu_button.click()

    # Espera hasta que aparezca el contenedor del menú lateral
    print("Esperando a que aparezca el menú lateral")
    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "bm-item-list"))
    )
    print("El menú lateral está visible.")

    menu_items = [
        ("inventory_sidebar_link", "All Items"),
        ("about_sidebar_link", "About"),
        ("logout_sidebar_link", "Logout"),
        ("reset_sidebar_link", "Reset App State")
    ]

    # Verifica que los enlaces requeridos estén presentes y con el texto correcto
    for item_id, expected_text in menu_items:
        element = driver.find_element(By.ID, item_id)
        assert element, f"No se encontró el enlace con id '{item_id}'"
        assert element.text == expected_text, f"Texto inesperado para '{item_id}': se esperaba '{expected_text}' pero se obtuvo '{element.text}'"

def verifica_filtro(driver):
    # Verifica que el elemento con clase active_option tenga el valor esperado
    print("Verificando que la opción activa sea 'Name (A to Z)'")
    active_option = driver.find_element(By.CLASS_NAME, "active_option")
    assert active_option, "No se encontró el elemento con clase active_option"
    assert active_option.text == "Name (A to Z)", f"Valor inesperado en active_option: se esperaba 'Name (A to Z)' pero se obtuvo '{active_option.text}'"

    # Verifica que el select de ordenamiento exista y tenga opciones
    print("Verificando la existencia del select de ordenamiento")
    sort_select = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert sort_select, "No se encontró el select con clase product_sort_container"
    options = sort_select.find_elements(By.TAG_NAME, "option")
    assert len(options) > 0, "El select no contiene opciones"

    expected_values = [
        "Name (A to Z)",
        "Name (Z to A)",
        "Price (low to high)",
        "Price (high to low)"
    ]

    # Verifica que las opciones estén en el orden esperado
    print("Verificando el orden y texto de las opciones")
    for index, expected_text in enumerate(expected_values):
        option_text = options[index].text
        assert option_text == expected_text, f"Texto inesperado en opción {index}: se esperaba {expected_text} pero se obtuvo {option_text}"

def verifica_carrito(driver):
    # Verifica que exista el carrito de compras
    print("Verificando la existencia del carrito de compras")
    carrito = driver.find_element(By.ID, "shopping_cart_container")
    assert carrito, "No se encontró el elemento con id shopping_cart_container"

    # Verifica que el carrito esté vacío (sin contador de cantidad)
    print("Verificando que el carrito esté vacío")
    contador = carrito.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(contador) == 0, "El carrito no está vacío: se encontró un contador de cantidad"
