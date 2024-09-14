"""
This script orchestrates the ETL (Extract, Transform, Load) process for medication data.

Functions:
- main: Main function to execute the ETL process.
"""

from src.extraction.extract_data import extract_data
from src.transformation.transform_data import transform_data
from src.loading.load_data import load_data
from src.utils.config import load_config
import os

def main():
    """
    Main function to execute the ETL process for extracting, transforming, and loading medication data.

    This function loads the configuration, extracts data from the input file, transforms it, and loads it into the output file.
    
    Returns
    -------
    None
    """
    # input_file = os.path.abspath('./data/input_urls.csv')
    # output_file = os.path.abspath('./data/output_data.csv')
    config = load_config()
    input_file = os.path.abspath(config['paths']['input_file'])
    output_file = os.path.abspath(config['paths']['output_file'])
    
    # Extracción de datos
    med_data = extract_data(input_file)
    
    # Transformación de datos
    transformed_df = transform_data(med_data)
    
    # Carga de datos
    load_data(transformed_df, output_file)

if __name__ == '__main__':
    main()