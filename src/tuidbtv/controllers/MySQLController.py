from textual.containers import Grid
from textual.validation import Number
from textual.widgets import Label, Input

from src.tuidbtv.controllers.DBController import DBController
import mysql.connector

from src.tuidbtv.enums_and_variables import CONNECTION_FIELD_CLASS


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
        return self.executeQueryWithHeaders(f"SELECT * FROM {schemaName}.{tableName} limit 100")

    def executeQuery(self, query_text: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_text)
            data = cursor.fetchall()
            return data
        except Exception as e:
            self.connection.rollback()
            raise e

    def executeQueryWithHeaders(self, query_text):
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

    @staticmethod
    def get_connection_form() -> Grid:
        return Grid(
            Label("Username"),
            Input(placeholder="root", id="userName", classes=CONNECTION_FIELD_CLASS),
            Label("Password"),
            Input(placeholder="", id="password", password=True, classes=CONNECTION_FIELD_CLASS),
            Label("Hostname/IP"),
            Input(placeholder="localhost", id="hostName", classes=CONNECTION_FIELD_CLASS),
            Label("Port"),
            Input(placeholder="3306", id="port", validators=[Number()], classes=CONNECTION_FIELD_CLASS),
            Label("Database"),
            Input(placeholder="mysql", id="database", classes=CONNECTION_FIELD_CLASS),
            id="connection_form"
        )