from controllers.MySQLController import MySQLController
from controllers.PostgresController import PostgresController


class ControllerFactory:
    @staticmethod
    def getController(data):
        match data['connectionType']:
            case "postgresql":
                return PostgresController(data['database'], data['userName'], data['password'], data['hostName'], data['port'])

            case "mysql":
                return MySQLController(data['database'], data['userName'], data['password'], data['hostName'], data['port'])