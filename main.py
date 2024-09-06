from src.extraction.extract_data import extract_data
from src.transformation.transform_data import transform_data
from src.loading.load_data import load_data
import os

def main():
    input_file = os.path.abspath('./data/input_urls.csv')
    output_file = os.path.abspath('./data/output_data.csv')
    
    # Extracción de datos
    med_data = extract_data(input_file)
    
    # Transformación de datos
    transformed_df = transform_data(med_data)
    
    # Carga de datos
    load_data(transformed_df, output_file)

if __name__ == '__main__':
    main()