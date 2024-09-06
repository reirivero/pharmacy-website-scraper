# import logging
import os
# from src.extraction.extract_data import med_data
# import pandas as pd

# file_path = os.path.abspath('data/output_urls.csv')

# output_data = []

def load_data(df,output_file):
    # Verificar si el archivo ya existe
    file_exists = os.path.isfile(output_file)
    
    # Guardar el DataFrame en el archivo
    df.to_csv(output_file, mode='a', header=not file_exists, index=False)
