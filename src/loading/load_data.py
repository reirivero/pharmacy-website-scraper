# import logging
import os
from src.extraction.extract_data import med_data
import pandas as pd

file_path = os.path.abspath('data/output_urls.csv')

output_data = []

def load_data(data):
    # logging.info("Cargando datos en la base de datos")
    # Código para cargar los datos en la base de datos
    for name, pharmacy in data.items():
        for pharmacy, rowdata in pharmacy.items():
            output_data.append(rowdata)

    df = pd.DataFrame(output_data)
    df.to_csv(file_path, index=False)

if __name__ == '__main__':
    load_data(med_data)
