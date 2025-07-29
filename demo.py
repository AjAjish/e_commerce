import os 
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('DB_PASSWORD')
DB_ROOT = os.getenv('DB_ROOT')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
print(f"DB_PASSWORD: {password}, DB_ROOT: {DB_ROOT}, DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}, DB_NAME: {DB_NAME}")