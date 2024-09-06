# import sys
# import os

# Agregar el directorio src al sys.path
# sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

# Ahora intenta importar med_data
# from extraction.extract_data import med_data
import pandas as pd
import numpy as np


def transform_data(med_data):
    output_data = []
    for name, pharmacy in med_data.items():
        for pharmacy, rowdata in pharmacy.items():
            output_data.append(rowdata)
    
    df = pd.DataFrame(output_data)
    print(df.head(20))
    print(df.dtypes)
    print(df['price'])
    df = df.replace({None : np.nan})
    df['date'] = pd.to_datetime(df['date'])
    # df['is_available'] = df['is_available'].astype('boolean')
    # df['bioequivalent'] = df['bioequivalent'].astype('boolean')
    df['active_principle'] = df['active_principle'].str.title()
    df['lab_name'] = df['lab_name'].str.title()
    def clean_price(prc):
        # Eliminar símbolos de moneda y caracteres no numéricos
        prc = str(prc).replace('$', '').replace(',', '')
        # Eliminar decimales si existen
        if '.' in prc and prc.endswith('.0'):
            prc = prc.rstrip('.0')
        # Eliminar puntos de separación de miles
        prc = prc.replace('.', '')
        return int(prc)
    df['price'] = df['price'].apply(clean_price)

    return df