import psycopg

from controllers.DBController import DBController


class PostgresController(DBController):
    def __init__(self, _dbname, _user, _password, _host, _port):
        self.connection = psycopg.connect(dbname=_dbname, user=_user, password=_password, host=_host,
                                          port=_port)

    def executeQuery(self, query_text):
        try:
            data = self.connection.cursor().execute(query_text).fetchall()
            self.connection.commit()
            return data
        except:
            self.connection.commit()
            raise

    def getSchemaNames(self):
        return self.executeQuery("SELECT distinct table_schema FROM information_schema.tables")

    def getTableNamesBySchema(self, schemaName):
        return self.executeQuery(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{schemaName}'")

    def getTablePreview(self, schemaName, tableName):
        data = self.executeQuery(f"SELECT * FROM {schemaName}.{tableName} limit 100")
        cutted_data = []
        for row in data:
            cutted_data.append(
                tuple(
                    str(cell)[:50] for cell in row
                )
            )
        headers = self.executeQuery(
            f"SELECT column_name from information_schema.columns where table_name = '{tableName}'")
        tableData = []
        headerData = tuple(column_name[0] for column_name in headers)
        tableData.append(headerData)
        for row in cutted_data:
            tableData.append(row)
        return tableData