import configparser
import os

current_directory = os.path.dirname(__file__)  # Assuming this script is in the same directory as config.ini

config_file_path = os.path.join(current_directory, 'data', 'config.ini')

config = configparser.ConfigParser()

config.read(config_file_path)


mysql_username = os.environ.get('mysql_username')
if mysql_username is None:
    mysql_username = config.get('ENVIRONMENT', 'mysql_username', fallback='default_value')

mysql_password = os.environ.get('mysql_password')
if mysql_password is None:
    mysql_password = config.get('ENVIRONMENT', 'mysql_password', fallback='default_value')

mysql_host = os.environ.get('mysql_host')
if mysql_host is None:
    mysql_host = config.get('ENVIRONMENT', 'mysql_host', fallback='default_value')

mysql_port = os.environ.get('mysql_port')
if mysql_port is None:
    mysql_port = config.get('ENVIRONMENT', 'mysql_port', fallback='default_value')

mysql_schema = os.environ.get('mysql_schema')
if mysql_schema is None:
    mysql_schema = config.get('ENVIRONMENT', 'mysql_schema', fallback='default_value')


temp_file_path = os.environ.get('temp_file_path')
if temp_file_path is None:
    temp_file_path = config.get('ENVIRONMENT', 'temp_file_path', fallback='default_value')

db_name = os.environ.get('db_name')
if db_name is None:
    db_name = config.get('ENVIRONMENT', 'db_name', fallback='default_value')