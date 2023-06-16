from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.validation import Length, Number
from textual.widgets import Select, Label, Input, Button, Placeholder

from config.ConfigParser import ConfigParser


class NewConnection(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Select([("postgresql", "postgresql"), ("mysql", "mysql")], allow_blank=False, value="postgresql", id="new_connection_type"),
            Label("Connection name"),
            Input(id="new_connection_name", validators=[Length(minimum=1)]),
            Label("Username"),
            Input(placeholder="postgres", id="new_connection_username"),
            Label("Password"),
            Input(placeholder="", id="new_connection_password", password=True),
            Label("Hostname/IP"),
            Input(placeholder="localhost", id="new_connection_hostname"),
            Label("Port"),
            Input(placeholder="5432", id="new_connection_port", validators=[Number()]),
            Label("Database"),
            Input(placeholder="public", id="new_connection_database"),
            Button("Cancel", disabled=False),
            Placeholder(),
            Button("Save", id="save_connection_button", disabled=True),
            id="new_connection_dialog"
        )

    def on_button_pressed(self, event):
        if event.button.id == "save_connection_button":
            connectionType: Select = self.query_one("#new_connection_type", expect_type=Select)
            connectionName: Input = self.query_one("#new_connection_name", expect_type=Input)
            hostName: Input = self.query_one("#new_connection_hostname", expect_type=Input)
            userName: Input = self.query_one("#new_connection_username", expect_type=Input)
            password: Input = self.query_one("#new_connection_password", expect_type=Input)
            port: Input = self.query_one("#new_connection_port", expect_type=Input)
            database: Input = self.query_one("#new_connection_database", expect_type=Input)
            data = {
                "connectionType": connectionType.value,
                "connectionName": connectionName.value,
                "hostName": hostName.value or hostName.placeholder,
                "userName": userName.value or userName.placeholder,
                "password": password.value or password.placeholder,
                "port": port.value or port.placeholder,
                "database": database.value or database.placeholder
            }
            ConfigParser.addNewConnection(data)
            self.dismiss(connectionName.value)
        else:
            self.app.pop_screen()

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        if event.input.id == "new_connection_name":
            if not event.value:
                self.query_one("#save_connection_button").disabled = True
            else:
                self.query_one("#save_connection_button").disabled = False
