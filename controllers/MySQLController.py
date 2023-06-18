from controllers.DBController import DBController
import mysql.connector

class MySQLController(DBController):
    def __init__(self, _dbname, _user, _password, _host, _port):
        self.connection = mysql.connector.connect(
            host=_host,
            user=_user,
            password=_password,
            port=_port)
    def getSchemaNames(self) -> list[str]:
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        return cursor.fetchall()

    def getTableNamesBySchema(self, schemaName: str) -> list[str]:
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW TABLES FROM `{schemaName}`")
        return cursor.fetchall()

    def getTablePreview(self, schemaName: str, tableName: str) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {schemaName}.{tableName} limit 100")
        myresult = cursor.fetchall()
        myresult.insert(0,next(zip(*cursor.description)))
        return myresult

    def executeQuery(self, queryText: str) -> list[dict]:
        pass


    def executyQueryWithHeaders(self, query_text):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_text)
            data = cursor.fetchall()
            header_data = tuple(column_name[0] for column_name in cursor.description)
            data.insert(0, header_data)
            return data
        except:
            self.connection.rollback()