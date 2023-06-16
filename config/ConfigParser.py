import json


class ConfigParser():
    @staticmethod
    def readConnectionList():
        with open("connections.json", 'r') as file:
            return json.load(file)["connections"]

    @staticmethod
    def addNewConnection(new_connection):
        with open('connections.json', 'r+') as file:
            json_data = json.load(file)
            json_data["connections"].append(new_connection)
            file.seek(0)
            json.dump(json_data, file)

    @staticmethod
    def removeConnectionByName(connection_name: str):
        with open('connections.json', 'r+') as file:
            json_data = json.load(file)
            json_data["connections"] = [
                connection
                for connection
                in json_data['connections']
                if connection['connectionName'] != connection_name
            ]
            file.seek(0)
            file.truncate(0)
            json.dump(json_data, file)
