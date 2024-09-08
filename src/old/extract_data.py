# import logging
import sys
import os

# Agregar el directorio src al sys.path
# sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from datetime import datetime
from src.utils import pharmacy as p
import pandas as pd

# Leer el archivo .csv
# file_path = os.path.abspath('../../data/input_urls.csv')
# input_data = pd.read_csv(file_path)

# med_data = {}

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

# # Principle function to call a specific function depending on the pharmacy
# def extract_data_one(url,product_name,pharmacy):
#     global data
#     data = {}

#     # Add info from input_urls.csv
#     data.update({
#         'date': datetime.now().strftime('%Y-%m-%d'),
#         'name': product_name,
#         'pharmacy': pharmacy
#     })

#     if 'buhochile.com' in url:
#         data = p.buhochile(url,data)
#     elif 'farmaciasahumada.cl' in url:
#         data = p.ahumada(url,data)
#     elif 'farmex.cl' in url:
#         data = p.farmex(url,data)
#     elif 'farmaciaelquimico.cl' in url:
#         data = p.elquimico(url,data)
#     elif 'salcobrand.cl' in url:
#         data = p.salcobrand(url,data)
#     elif 'novasalud.cl' in url:
#         data = p.novasalud(url,data)
#     elif 'drsimi.cl' in url:
#         data = p.drsimi(url,data)
#     elif 'ecofarmacias.cl' in url:
#         data = p.ecofarmacias(url,data)
#     elif 'mercadofarma.cl' in url:
#         data = p.mercadofarma(url,data)
#     elif 'farmaciameki.cl' in url:
#         data = p.meki(url,data)
#     else:
#         pass

#     # update the dict
#     if product_name not in med_data:
#         med_data[product_name] = {}
#     med_data[product_name][pharmacy] = data 


# # Iterar sobre cada fila del DataFrame
# for index, row in input_data.iterrows():
#     url = row['url']
#     product_name = row['product_name']
#     pharmacy = row['pharmacy']
    
#     # Llamar a la función de extracción con los valores de la fila
#     extract_data_one(url, product_name, pharmacy)
#     # print(med_data)
    

def extract_data(file_path):
    input_data = pd.read_csv(file_path)
    med_data = {}

    for index, row in input_data.iterrows():
        url = row['url']
        product_name = row['product_name']
        pharmacy = row['pharmacy']
        print(url)
        data = {}

        # Add info from input_urls.csv
        data.update({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'name': product_name,
            'pharmacy': pharmacy
        })

        if 'buhochile.com' in url:
            data = p.buhochile(url,data)
        elif 'farmaciasahumada.cl' in url:
            data = p.ahumada(url,data)
        elif 'farmex.cl' in url:
            data = p.farmex(url,data)
        elif 'farmaciaelquimico.cl' in url:
            data = p.elquimico(url,data)
        elif 'salcobrand.cl' in url:
            data = p.salcobrand(url,data)
        elif 'novasalud.cl' in url:
            data = p.novasalud(url,data)
        elif 'drsimi.cl' in url:
            data = p.drsimi(url,data)
        elif 'ecofarmacias.cl' in url:
            data = p.ecofarmacias(url,data)
        elif 'mercadofarma.cl' in url:
            data = p.mercadofarma(url,data)
        elif 'farmaciameki.cl' in url:
            data = p.meki(url,data)
        elif 'cruzverde.cl' in url:
            data = p.cruzverde(url,data)
        elif 'profar.cl' in url:
            data = p.profar(url,data)
        elif 'farmaciasknop.com' in url:
            data = p.knoplab(url,data)
        else:
            pass

        # update the dict
        if product_name not in med_data:
            med_data[product_name] = {}
        med_data[product_name][pharmacy] = data
        # print(med_data)
    
    return med_data