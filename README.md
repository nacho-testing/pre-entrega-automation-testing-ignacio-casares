# Proyecto de Automatización de Pruebas (SauceDemo)

## Propósito del proyecto
Este proyecto implementa una automatización de pruebas para el sitio **SauceDemo** (https://www.saucedemo.com/), utilizando **Selenium WebDriver** y **Python**.

El objetivo es automatizar los flujos en la página SauceDemo y garantizar que las funciones críticas del sitio web se comporten como se espera mediante pruebas automatizadas.

## Tecnologías utilizadas
- **Python 3**
- **pytest**
- **pytest-html**
- **Selenium WebDriver**

## Estructura

 - **README.md** - Documentación del proyecto
 - **tests/test_saucedemo.py** — Casos de prueba
 - **utils/helpers.py** — Configuración del WebDriver (Chrome) y funciones auxiliares para los tests
 - **reports/** - Reportes HTML y capturas de pantalla

## Instalación

1. Asegúrate de tener Python 3.7 o superior instalado
2. Descarga el WebDriver correspondiente a tu navegador: [selenium.dev](https://www.selenium.dev/)
3. Clona este repositorio:
   ```bash
   git clone TODO
4. Instala las dependencias:
   ```bash
    pip install selenium pytest pytest-html

## Casos de prueba
 - **test_login**: Verifica acceso correcto a la página de inventario.
 - **test_catalogo**: Comprueba la presencia de productos, filtros y menú.
 - **test_carrito**: Valida que agregar un producto al carrito funcione correctamente.

## Ejecución

 - Ejecuta las pruebas con:
    ```bash
    pytest -v tests/test_saucedemo.py
 - Para generar un reporte HTML:
    ```bash
    pytest tests/test_saucedemo.py -v --html=./reports/reporte.html

## Autor
**Autor**: NACHO