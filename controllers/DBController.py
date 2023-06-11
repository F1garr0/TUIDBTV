class DBController():
    def getSchemaNames(self) -> list[str]:
        pass

    def getTableNamesBySchema(self, schemaName: str) -> list[str]:
        pass

    def getTablePreview(self, schemaName: str, tableName: str) -> list[dict]:
        pass

    def executeQuery(self, queryText: str) -> list[dict]:
        pass
