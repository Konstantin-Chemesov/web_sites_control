from dotenv import dotenv_values

dotenv_params = dotenv_values(".env")
PROJECT_HOST = dotenv_params.get('PROJECT_HOST', '')
PROJECT_PORT = int(dotenv_params.get('PROJECT_PORT', ''))
DB_PORT = int(dotenv_params.get('DB_PORT', ''))
DB_NAME = dotenv_params.get('DB_NAME', '')
DB_TEST_NAME = 'db_test'
DB_USERNAME = dotenv_params.get('DB_USERNAME', '')
DB_PASSWORD = dotenv_params.get('DB_PASSWORD', '')