<<<<<<< HEAD
import logging

def load_data(data):
    logging.info("Cargando datos en la base de datos")
    # Código para cargar los datos en la base de datos
=======
"""
This module contains functions to load data into CSV files.

Functions:
- load_data: Loads a pandas DataFrame into a CSV file, appending if the file already exists.
"""

import os

def load_data(df,output_file):
    """
    Loads a pandas DataFrame into a CSV file, appending if the file already exists.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame to be loaded into the CSV file.
    output_file : str
        The name of the output CSV file.

    Returns
    -------
    None
    """
    # Check if the file already exists
    file_exists = os.path.isfile(output_file)
    
    # Save the DataFrame to the file
    df.to_csv(output_file, mode='a', header=not file_exists, index=False)
>>>>>>> feature/improve-etl-scraping
