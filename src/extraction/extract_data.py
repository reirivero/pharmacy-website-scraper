import logging
import time
import json
import pandas as pd

# Leer el archivo .csv
input_data = pd.read_csv('../../data/input_urls.csv')

print(input_data.head(10))
for row in input_data:
    print(row, type(row),sep='\n')

if __name__ == '__main__':
    pass