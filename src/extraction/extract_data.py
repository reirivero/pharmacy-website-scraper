from datetime import datetime
from src.utils import pharmacy as p
import pandas as pd
import logging
from src.utils.config import load_config

# Configurar el logging
# logging.basicConfig(filename='extract_data.log', level=logging.ERROR, 
#                     format='%(asctime)s:%(levelname)s:%(message)s')

config = load_config()
logging.basicConfig(filename=config['paths']['log_file'], 
                    level=config['logging']['level'], 
                    format=config['logging']['format'])

# Example of the dictionary 
'''
med_data = {
    'Hormogel' : {
        "Salcobrand" : {
            "date" : datetime.now().strftime('%Y-%m-%d'),
            "name": product_name,
            "pharmacy" : pharmacy,
            "web_name": name,
            "is_available": is_available,
            "price": price,
            "bioequivalent": bioequivalent,
            "active_principle": active_principle,
            "sku": sku,
            "lab_name": lab_name
        },
        "El Búho" : {
            "date" : datetime.now().strftime('%Y-%m-%d'),
            "name": product_name,
            "pharmacy" : pharmacy,
            "web_name": name,
            "is_available": is_available,
            "price": price,
            "bioequivalent": bioequivalent,
            "active_principle": active_principle,
            "sku": sku,
            "lab_name": lab_name
        }      
    },
    'Rosuvastatina' : {
        "Salcobrand : {
            "date" : datetime.now().strftime('%Y-%m-%d'),
            "name": product_name,
            "pharmacy" : pharmacy,
            "web_name": name,
            "is_available": is_available,
            "price": price,
            "bioequivalent": bioequivalent,
            "active_principle": active_principle,
            "sku": sku,
            "lab_name": lab_name
        }
    },
}
'''

def extract_data(file_path):
    input_data = pd.read_csv(file_path)
    med_data = {}

    for index, row in input_data.iterrows():
        url = row['url']
        product_name = row['product_name']
        pharmacy = row['pharmacy']
        print(url)

        # Add info from input_urls.csv
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'name': product_name,
            'pharmacy': pharmacy,
            'price': None,
            'lab_name': None,
            'bioequivalent': None,
            'is_available': None,
            'active_principle': None,
            'sku': None,
            # 'more_products': None,
            'web_name': None,
            'url': url
        }

        try:
            # Llamar a la función de scraping correspondiente
            if 'buhochile.com' in url:
                data.update(p.buhochile(url,data)) # type: ignore
            elif 'farmaciasahumada.cl' in url:
                data.update(p.ahumada(url,data)) # type: ignore
            elif 'farmex.cl' in url:
                data.update(p.farmex(url,data)) # type: ignore
            elif 'farmaciaelquimico.cl' in url:
                data.update(p.elquimico(url,data)) # type: ignore
            elif 'salcobrand.cl' in url:
                data.update(p.salcobrand(url,data)) # type: ignore
            elif 'novasalud.cl' in url:
                data.update(p.novasalud(url,data)) # type: ignore
            elif 'drsimi.cl' in url:
                data.update(p.drsimi(url,data)) # type: ignore
            elif 'ecofarmacias.cl' in url:
                data.update(p.ecofarmacias(url,data)) # type: ignore
            elif 'mercadofarma.cl' in url:
                data.update(p.mercadofarma(url,data)) # type: ignore
            elif 'farmaciameki.cl' in url:
                data.update(p.meki(url,data)) # type: ignore
            elif 'cruzverde.cl' in url:
                data.update(p.cruzverde(url,data)) # type: ignore
            elif 'profar.cl' in url:
                data.update(p.profar(url,data)) # type: ignore
            elif 'farmaciasknop.com' in url:
                data.update(p.knoplab(url,data)) # type: ignore
            else:
                raise ValueError(f"URL no reconocida: {url}")

        except Exception as e:
            logging.error(f"Error al procesar la URL {url}: {e}")
            continue

        # update the dict
        if product_name not in med_data:
            med_data[product_name] = {}
        med_data[product_name][pharmacy] = data
    
    return med_data