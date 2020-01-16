from config.config import Config
import pymssql
import pymysql

def get_connection(connection_name, server_type):
    config = Config()
    db_url = config.get(connection_name.upper(), 'datasource.url')
    db_user = config.get(connection_name.upper(), 'datasource.username')
    db_pass = config.get(connection_name.upper(), 'datasource.password')
    db_host = _parse_connection_host(db_url)
    db_database = _parse_database(db_url)

    if (server_type == 'mssql'):
        return pymssql.connect(host=db_host, user=db_user, password=db_pass)
    elif (server_type == 'mysql'):
        return pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database)

def _parse_connection_host(connection_string):
    if "/" in connection_string:
        if ";" in connection_string:
            return connection_string.split("/")[2] + "\\" + connection_string.split(";")[1].split("=")[1]
        else:
            return connection_string.split("/")[2]
    else:
        return(connection_string)

def _parse_database(connection_string):
    if "/" in connection_string:
        return connection_string.split("/")[3].split("?")[0]
    else:
        return(connection_string)