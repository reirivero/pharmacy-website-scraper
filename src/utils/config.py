<<<<<<< HEAD
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Definir las variables de entorno que se utilizarán en el proyecto
DATABASE_URL = os.getenv('DATABASE_URL')
API_KEY = os.getenv('API_KEY')

# Puedes agregar más configuraciones según sea necesario
=======
import yaml
import os

def load_config(config_path=os.path.abspath('./src/utils/config.yaml')):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
>>>>>>> feature/improve-etl-scraping
