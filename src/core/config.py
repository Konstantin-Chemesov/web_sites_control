import os

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'links_check')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_NAME = os.getenv('DB_NAME', 'base')
DB_USERNAME = os.getenv('DB_USERNAME', 'username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))