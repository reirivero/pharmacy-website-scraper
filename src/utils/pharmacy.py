# Importar las posibles librerías
import re
import json
# Beautiful Soup
from bs4 import BeautifulSoup
# Selenium  libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from .decorators import validate_data, handle_http_request, initialize_driver

# Grupo de funciones según la farmacia a ser escaneada

@handle_http_request
@validate_data(['price', 'lab_name', 'is_available', 'sku', 'web_name'])
def farmex(url, soup, data) -> dict:
    # Extract product name from web
    name = soup.find('h1', class_='page-heading').text.strip('"')

    # Extract price
    product_price_container = soup.find('div', class_='product-price')
    price = product_price_container.find('div', class_='detail-price').text.strip()

    # Extract stock y determinar si hay stock disponible
    stock_text = product_price_container.find('pre').text.strip()
    is_available = int(stock_text.split(': ')[1]) > 0
    
    # Extract JSON-LD script
    json_ld_script = soup.find('script', type='application/ld+json').string
    json_data = json.loads(json_ld_script)

    # Extract SKU and lab_name
    sku = json_data.get('sku', None)
    lab_name = json_data.get('brand', {}).get('name', None)

    data.update({
        'price': price,
        'lab_name': lab_name,
        'is_available': is_available,
        'sku': sku,
        'web_name': name,
    })

    return data

@handle_http_request
@validate_data(['price', 'bioequivalent','is_available','web_name'])
def salcobrand(url,soup, data) -> dict:
    # Buscar el script que contiene 'product_traker_data'
    script_tag = soup.find('script', string=re.compile(r'var product_traker_data ='))
    if not script_tag:
        return {}

    # Extraer el contenido del script
    script_content = script_tag.string

    # Extraer el JSON del script
    json_data = re.search(r'var product_traker_data = ({.*});', script_content).group(1) # type: ignore
    product_data = json.loads(json_data)

    # Extraer la información requerida
    name = product_data['name']
    is_available = product_data['isAvailable']
    price = product_data['price']
    bioequivalent = product_data['products'][list(product_data['products'].keys())[0]]['params']['bioequivalent']

    # Extraer el "Principio Activo" del meta tag
    meta_description = soup.find('meta', property='og:description')['content']
    active_principle_match = re.search(r'Principio Activo: ([^|]+)', meta_description)
    active_principle = active_principle_match.group(1).strip().split('/')[0].strip() if active_principle_match else None

    # Extraer el SKU de la URL
    sku_match = soup.find('span', class_='sku')
    sku = sku_match.text.split('\n')[2].strip() if sku_match else None

    # Extraer el nombre del laboratorio del bloque de código HTML proporcionado
    lab_name_tag = soup.find('div', class_='description-area').find('h4', string='Laboratorio')
    if lab_name_tag:
        if lab_name_tag.find_next_sibling('p'):
            lab_name = lab_name_tag.find_next_sibling('p').text.strip()
        else:
            lab_name = lab_name_tag.find_next_sibling('div').text.strip()
    else:
        lab_name = None

    data.update({
        'price': '$'+price,
        'lab_name': lab_name,
        'bioequivalent': bioequivalent,
        'is_available': is_available,
        'active_principle': active_principle,
        'sku': sku,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name', 'bioequivalent', 'is_available', 'active_principle', 'web_name'])
def buhochile(url,soup,data) -> dict:    
    # Encontrar el script que contiene los datos JSON
    script = soup.find('script', {'id': '__NEXT_DATA__'})
    json_data = json.loads(script.string) # type: ignore

    # Extraer los valores requeridos
    product = json_data['props']['pageProps']['product']
    name = f'{product['name']} {product['tablets']} {product['pharmaceuticForm']}'
    active_principle = product['activePrinciple']
    price = f'${product['minPrice']}'
    bioequivalent = product['bioequivalent']
    lab_name = product['laboratory']['name']

    # Extraer la disponibilidad del producto
    meta_availability = soup.find('meta', {'property': 'product:availability'})
    is_available = meta_availability['content'] == 'in stock' # type: ignore

    data.update({
        'price': price,
        'lab_name': lab_name,
        'bioequivalent': bioequivalent,
        'is_available': is_available,
        'active_principle': active_principle,
        "web_name": name
    })

    return data

@validate_data(['price', 'lab_name', 'is_available', 'active_principle', 'sku', 'web_name'])
@handle_http_request
@initialize_driver
def elquimico(url, driver, soup, data) -> dict:
    try:
        driver.get(url)
    except WebDriverException as e:
        raise Exception(f"Error al cargar la página: {e}")

    wait = WebDriverWait(driver, 10)
    price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.money-subtotal')))

    # Avaiibity - stock 
    stock_elem = soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['productView-info-value'] and ('En stock' in tag.text or 'Agotado' in tag.text))

    elem_product = soup.find('h1',{'class':'productView-title'})
    name = elem_product.get_text().strip() if elem_product \
        else "Name product not found"  
 
    price = price_element.text
    is_available = True if stock_elem.text.strip() == 'En stock' else False # type: ignore

    sku_elem = soup.find_all('span',class_='productView-info-value')
    sku = (list(sku_elem))[1].text.strip()

    # Encontrar el contenedor del principio activo
    tab_content = soup.find('div', class_='tab-popup-content')
    active_principle = tab_content.find('strong').text # type: ignore

    # Encontrar el contenedor del vendedor
    vendor_container = soup.find('div', class_='productView-info-item')
    lab_name = vendor_container.find('span', class_='productView-info-value').text.strip() # type: ignore
    
    driver.quit()

    data.update({
        'price': price,
        'lab_name': lab_name,
        'is_available': is_available,
        'active_principle': active_principle,
        'sku': sku,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name', 'is_available', 'active_principle', 'web_name'])
def ahumada(url,soup,data) -> dict:
    # Extraer el Principio Activo
    active_principle = soup.find('th', string='Principio Activo').find_next_sibling('td').text.strip() # type: ignore

    # Extraer el Laboratorio
    lab_name = soup.find('th', string='Laboratorio').find_next_sibling('td').text.strip() # type: ignore

    # Extraer el Nombre del Producto
    name = soup.find('h1', class_='product-name').text.strip() # type: ignore

    # Extraer el Precio
    price = soup.find('span', class_='value d-flex align-items-center').text.strip() # type: ignore
    # Verificar la disponibilidad del producto
    add_to_cart_button = soup.find('button', class_='add-to-cart btn btn-primary')
    is_available = 'Agregar al carrito' in add_to_cart_button.text  # type: ignore

    data.update({
        'price': price,
        'lab_name': lab_name,
        'is_available': is_available,
        'active_principle': active_principle,
        'web_name': name,
    })

    return data

@handle_http_request
@validate_data(['price', 'is_available', 'sku', 'web_name'])
def ecofarmacias(url,soup,data) -> dict:
    # Extraer el precio
    price = soup.find('bdi').text

    # Extraer el valor de stock
    stock_elemt = soup.find('p', class_=re.compile(r'stock'))
    
    add_to_cart_button = soup.find('button', class_='single_add_to_cart_button button alt')
    
    is_available = False
    if stock_elemt:
        is_available = True if stock_elemt.text.strip() != 'Sin existencias' else False # type: ignore 
    elif add_to_cart_button:
        is_available = True if 'Añadir al carrito' in add_to_cart_button.text.strip() else False

    # Extraer el SKU
    sku = soup.find('span', class_='sku').text.strip() # type: ignore

    # Extraer los principios activos
    active_principle_elem = soup.find('li', string=lambda x: x and 'Principios Activos:' in x) # type: ignore
    if active_principle_elem:
        active_principle = active_principle_elem.text.split(': ')[1]
    else: 
        active_principle = None

    # Extraer el nombre del producto y laboratorios
    product_title = soup.find('h1', class_='product_title entry-title').text
    name = product_title.split('(')[0].strip()

    data.update({
        'price': price,
        'is_available': is_available,
        'active_principle': active_principle,
        'sku': sku,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price','bioequivalent','is_available', 'sku', 'web_name'])
def drsimi(url,soup,data) -> dict:
    # Encontrar el contenedor del precio
    price_container = soup.find('span', class_='vtex-product-price-1-x-currencyContainer')

    # Encontrar el contenedor del precio con rebaja
    price_container = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')

    # Extraer y formatear el precio
    currency_code = price_container.find('span', class_='vtex-product-price-1-x-currencyCode').text
    currency_integer = price_container.find_all('span', class_='vtex-product-price-1-x-currencyInteger')
    currency_group = price_container.find('span', class_='vtex-product-price-1-x-currencyGroup').text

    # Formatear el precio
    price = f"{currency_code}{currency_integer[0].text}{currency_group}{currency_integer[1].text}"

    # Encontrar el SKU
    sku_container = soup.find('span', class_='vtex-product-identifier-0-x-product-identifier__value')
    sku = sku_container.text.strip()

    # Encontrar nombre del producto
    name_container = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview')
    name = name_container.text.strip()

    # Encontrar el contenedor del texto de bioequivalencia
    bioequivalent_elem = soup.find('p', class_='farmaciasdeldrsimicl-theme-2-x-bioequivalenteText')
    if bioequivalent_elem:
        bioequivalent_text = bioequivalent_elem.text
        # Verificar si el texto contiene "es bioequivalente"
        bioequivalent = "es bioequivalente" in bioequivalent_text
    else: 
        bioequivalent = False

    # Extraer el principio activo
    active_principle_elem = soup.find('td', class_='vtex-store-components-3-x-specificationItemSpecifications--principioActivo')
    if active_principle_elem:
        active_principle = active_principle_elem.text.strip()
    else: 
        active_principle = None

    # Verificar la disponibilidad del producto
    add_to_cart_button = soup.find('button', class_='vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-regular t-action bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer w-100')
    product_availability = bool(add_to_cart_button)
    is_available = True if product_availability else False

    data.update({
        'price': price,
        'bioequivalent': bioequivalent,
        'is_available': is_available,
        'active_principle': active_principle,
        'sku': sku,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name','is_available', 'active_principle', 'sku', 'web_name'])
def novasalud(url,soup,data) -> dict:
    name = soup.find('span', class_='base', itemprop='name').text.strip()

    # Extraer el SKU
    sku = soup.find('div', class_='value', itemprop='sku').text.strip()

    # Extraer el Precio
    price = soup.find('span', class_='price').text.strip()

    # Extraer el Stock y determinar si hay stock disponible
    stock_text = soup.find('div', class_='stock available').find('span').text.strip()
    is_available = stock_text == 'En stock'

    # Extraer el Principio Activo
    active_principle = soup.find('th', string='Principio Activo (DCI)').find_next_sibling('td').text.strip()

    # Extraer el Laboratorio
    lab_name = soup.find('th', string='Laboratorio').find_next_sibling('td').text.strip()
 
    data.update({
        'price': price,
        'lab_name': lab_name,
        'is_available': is_available,
        'active_principle': active_principle,
        'sku': sku,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name', 'is_available', 'web_name'])
def mercadofarma(url, soup,data) -> dict:
    name = soup.find('h1', class_='product-meta__title').text.strip()

    # Extraer el Laboratorio (Vendor)
    lab_name = soup.find('a', class_='product-meta__vendor').text.strip()

    # Extraer el Precio
    price = soup.find('span', class_='price').contents[-1].strip()

    # Extraer la cantidad en stock y determinar si hay stock disponible
    stock_text = soup.find('span', class_='product-form__inventory').text.strip()
    is_available = 'quedan' in stock_text and '0' not in stock_text
    
    data.update({
        'price': price,
        'lab_name': lab_name,
        'is_available': is_available,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name', 'bioequivalent','is_available', 'active_principle', 'web_name'])
def meki(url,soup, data) -> dict:
    # Encontrar el script con el JSON
    script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')
    json_data = json.loads(script_tag.string)
    
    # Extraer los datos necesarios
    product_data = json_data['props']['pageProps']['initialProduct']
    
    bioequivalent = product_data['isBioequivalent']
    active_principle = product_data['activePrinciple']
    lab_name = product_data['laboratory']
    name = product_data['name']
    price = product_data['price']
    is_available = False
    for p_tag in soup.find_all('p', class_='MuiTypography-root MuiTypography-body1 mui-style-m99pms'):
        if 'Recibe' in p_tag.text and 'mañana' in p_tag.text:
            is_available = True
            break
    
    data.update({
        'price': price,
        'lab_name': lab_name,
        "bioequivalent": bioequivalent,
        'is_available': is_available,
        'active_principle': active_principle,
        'web_name': name
    })

    return data

@validate_data(['price', 'lab_name','web_name'])
@handle_http_request
@initialize_driver
def cruzverde(url, driver, soup, data) -> dict:
    try:
        driver.get(url)

        # Esperar a que el app-root esté presente
        app_root = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-root"))
        )

        # Obtener el contenido de <app-root>
        app_root_content = app_root.get_attribute('innerHTML')
        soup = BeautifulSoup(app_root_content, 'html.parser') # type: ignore

        # Encontrar y hacer clic en el botón "Aceptar"
        accept_button = soup.find('button', text='Aceptar')
        if accept_button:
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(text(), 'Aceptar')]"))

        # Recargar la página
        driver.get(url)

        # Esperar a que el nuevo app-root esté presente
        app_root = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-root"))
        )

        # Obtener el contenido de <app-root>
        app_root_content = app_root.get_attribute('innerHTML')

        # Analizar el contenido con BeautifulSoup
        soup = BeautifulSoup(app_root_content, 'html.parser') # type: ignore

        # Extraer el precio
        price_element = soup.find('span', class_='font-bold text-prices text-16')
        price = price_element.text if price_element else None

        # Extraer el nombre y el laboratorio
        laboratory_element = soup.find('span', class_='text-12 uppercase italic cursor-pointer hover:text-accent')
        lab_name = laboratory_element.text if laboratory_element else None

        name_element = soup.find('h1', class_='text-18 leading-22 font-bold w-3/4 mb-5')
        name = name_element.text.strip('"').strip() if name_element else None

        # more_products_span = soup.find(lambda tag: tag.name == 'span' and 
        #              tag.get('class') == ['ng-star-inserted'] and 
        #              tag.text == "Productos más")
        # # print(more_products_span.text.strip() if more_products_span else 'Not available "Productos Más"')
        # print(more_products_span.text.strip() if more_products_span else 'Not Productos más') 
        # more_products = True if more_products_span else False 
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar el navegador
        driver.quit()

    data.update({
        'price': price,
        'lab_name': lab_name.strip(), # type: ignore
        'web_name': name      
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name','is_available', 'active_principle', 'sku', 'web_name'])
def profar(url, soup, data) -> dict:
    # Extraer el Principio Activo
    active_principle = soup.find('td', {'data-specification': 'Principio Activo'}).find_next_sibling('td').text.strip()

    # Extraer el nombre del medicamento, SKU, precio y laboratorio
    title = soup.find('title').text.strip()
    name = title.split(' ')[0]
    sku = title.split(' ')[1]

    meta_tags = soup.find_all('meta', {'data-react-helmet': 'true'})
    lab_name = None

    for tag in meta_tags:
        if tag.get('property') == 'product:price:amount':
            price = tag.get('content')
        elif tag.get('property') == 'product:brand':
            lab_name = tag.get('content')

    # Verificar si el botón "Comprar" está activo
    boton_comprar = soup.find('button', text='Comprar')
    is_available = boton_comprar and 'disabled' not in boton_comprar.attrs
    data.update({
        'price': '$'+price,
        'lab_name': lab_name,
        'is_available': is_available,
        'active_principle': active_principle,
        'sku': sku,
        'web_name': name
    })

    return data

@handle_http_request
@validate_data(['price', 'lab_name', 'is_available', 'sku', 'web_name'])
def knoplab(url, soup,data) -> dict:
    json_ld_script = soup.find('script', type='application/ld+json').string
    json_ld = json.loads(json_ld_script)

    sku = json_ld.get('sku', None)
    price = json_ld.get('offers', {}).get('lowPrice')
    lab_name = json_ld.get('brand',{}).get('name',None)
    name = json_ld.get('name', None)

    stock_span = soup.find_all('span', class_='units-in-stock')

    stock_p = soup.find('p', class_='units-in-stock')
    
    if stock_span:
        if len(stock_span) > 1:
            stock_available = [int(st.text.strip().split(':')[1].strip()) > 0 for st in stock_span ]
            is_available = True if any(stock_available) else False
        else:
            stock = stock_span.text.strip().split(':')[1].strip()
            is_available = True if int(stock) > 0 else False
    elif stock_p:
            stock = stock_p.text.strip().split(':')[1].strip()
            is_available = True if int(stock) > 0 else False
    else:
        is_available = False

    data.update({
        'price': '$'+price,
        'lab_name': lab_name,
        'is_available': is_available,
        'sku': sku,
        'web_name': name
    })

    return data