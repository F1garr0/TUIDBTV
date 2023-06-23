from controllers.DBController import DBController
import mysql.connector


class MySQLController(DBController):
    def __init__(self, _dbname, _user, _password, _host, _port):
        self.connection = mysql.connector.connect(
            host=_host,
            user=_user,
            password=_password,
            port=_port,
            database=_dbname)

    def getSchemaNames(self):
        return self.executeQuery("SHOW DATABASES")

    def getTableNamesBySchema(self, schemaName: str):
        return self.executeQuery(f"SHOW TABLES FROM `{schemaName}`")

    def getTablePreview(self, schemaName: str, tableName: str):
        return self.executyQueryWithHeaders(f"SELECT * FROM {schemaName}.{tableName} limit 100")

    def executeQuery(self, query_text: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_text)
            data = cursor.fetchall()
            return data
        except Exception as e:
            self.connection.rollback()
            raise e

    def executyQueryWithHeaders(self, query_text):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_text)
            data = cursor.fetchall()
            header_data = tuple(column_name[0] for column_name in cursor.description)
            data.insert(0, header_data)
            return data
        except Exception as e:
            self.connection.rollback()
            raise e
