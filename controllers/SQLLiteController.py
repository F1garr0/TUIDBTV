import sqlite3

from textual.containers import Grid
from textual.widgets import Label, Input

from controllers.DBController import DBController


class SQLLiteController(DBController):

    def __init__(self, _db_path):
        self.connection = sqlite3.connect(_db_path)

    def getSchemaNames(self) -> list[str]:
        return ['tables']

    def getTableNamesBySchema(self, schemaName: str) -> list[str]:
        return self.executeQuery("SELECT name FROM sqlite_master WHERE type='table';")

    def getTablePreview(self, schemaName: str, tableName: str) -> list[dict]:
        return self.executeQueryWithHeaders(f"select * from {tableName} limit 50;")

    def executeQuery(self, queryText: str) -> list[str]:
        cursor = self.connection.cursor()
        cursor.execute(queryText)
        return cursor.fetchall()

    def executeQueryWithHeaders(self, queryText: str):
        cursor = self.connection.cursor()
        cursor.execute(queryText)
        data = cursor.fetchall()
        data.insert(0, next(zip(*cursor.description)))
        return data

    @staticmethod
    def get_connection_form():
        return Grid(
            Label("DataBase path"),
            Input(placeholder=":memory:", id="new_connection_username"),
            id="connection_form"
        )
