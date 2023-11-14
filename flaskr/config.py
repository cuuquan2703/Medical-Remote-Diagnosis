import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(__file__, '.env')
load_dotenv(dotenv_path)

STATIC = os.environ.get('STATIC')

DB_TABLE = os.environ.get('DB_TABLE')
DB_PORT = os.environ.get('DB_PORT')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

HASHING_METHOD = os.environ.get('HASHING_METHOD')