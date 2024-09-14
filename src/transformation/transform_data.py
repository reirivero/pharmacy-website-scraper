
"""
This module contains functions to transform medication data.

Functions:
- transform_data: Transforms medication data into a pandas DataFrame with cleaned and formatted columns.
"""

import pandas as pd
import numpy as np


def transform_data(med_data):
    """
    Transforms medication data into a pandas DataFrame with cleaned and formatted columns.

    Parameters
    ----------
    med_data : dict
        A dictionary containing medication data.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with transformed medication data.
    """
    output_data = []
    for name, pharmacy in med_data.items():
        for pharmacy, rowdata in pharmacy.items():
            output_data.append(rowdata)

    df = pd.DataFrame(output_data)
    pd.set_option('future.no_silent_downcasting', True)
    df = df.replace({None: np.nan})
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Aplicar transformaciones solo a las filas que no son NaN
    df['active_principle'] = df['active_principle'].apply(lambda x: x.title() if isinstance(x, str) else x)
    df['lab_name'] = df['lab_name'].apply(lambda x: x.title() if isinstance(x, str) else x)
    
    
    def clean_price(prc):
        if pd.isna(prc):
            return prc
        # Eliminar símbolos de moneda y caracteres no numéricos
        prc = str(prc).replace(' ', '').replace('$', '').replace(',', '')
        # Eliminar decimales si existen
        if '.' in prc and prc.endswith('.0'):
            prc = prc.rstrip('.0')
        # Eliminar puntos de separación de miles
        prc = prc.replace('.', '')
        return int(prc)

    df['price'] = df['price'].apply(clean_price)

    # Renombrar las columnas
    df = df.rename(columns={
        'date': 'Fecha',
        'name': 'Nombre del Remedio',
        'pharmacy': 'Farmacia',
        'price': 'Precio',
        'lab_name': 'Laboratorio',
        'bioequivalent': '¿Es Bioequivalente?',
        'is_available': '¿Stock?',
        'active_principle': 'Principio Activo',
        'sku': 'SKU',
        # 'more_products': 'Cruz Verde - ¿Productos más?',
        'web_name': 'Nombre (webpage)',
        'url': 'URL'
    })

    return df