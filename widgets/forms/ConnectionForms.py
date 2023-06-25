from textual.app import ComposeResult
from textual.widget import Widget

from controllers.MySQLController import MySQLController
from controllers.PostgresController import PostgresController
from controllers.SQLLiteController import SQLLiteController


class ConnectionForms(Widget):

    DEFAULT_CSS = """
        ConnectionForms{ column-span: 3; }
    """

    def __init__(self, connectionType: str):
        super().__init__()
        self.form = None
        self.selectForm(connectionType)

    def compose(self) -> ComposeResult:
        yield self.form()

    def selectForm(self, connectionType: str):
        #TODO move to Controller_factory
        match connectionType:
            case "postgresql":
                self.form = PostgresController.get_connection_form
            case "mysql":
                self.form = MySQLController.get_connection_form
            case _:
                self.form = SQLLiteController.get_connection_form

    def changeForm(self, connectionType: str):
        fields = self.query_one('#connection_form')
        fields.remove()
        self.selectForm(connectionType)
        self.mount(self.form())