from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.validation import Length, Number
from textual.widgets import Select, Label, Input, Button, Placeholder

from config.ConfigParser import ConfigParser
from widgets.forms.ConnectionForms import ConnectionForms


class NewConnection(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Select([("postgresql", "postgresql"), ("mysql", "mysql"), ("sqlite", "sqlite")], allow_blank=False,
                   value="postgresql",
                   id="new_connection_type"),
            Label("Connection name *"),
            Input(id="new_connection_name", validators=[Length(minimum=1)]),
            ConnectionForms("postgresql"),
            Button("Cancel", disabled=False),
            Placeholder(),
            Button("Save", id="save_connection_button", disabled=True),
            id="new_connection_dialog"
        )

    def on_button_pressed(self, event):
        if event.button.id == "save_connection_button":
            connection_data = {}
            connectionType: Select = self.query_one("#new_connection_type", expect_type=Select)
            connectionName: Input = self.query_one("#new_connection_name", expect_type=Input)
            connection_data['connectionType'] = connectionType.value
            connection_data['connectionName'] = connectionName.value

            data_fields = self.query(".CONNECTION_DATA_FIELD")
            for field in data_fields.nodes:
                connection_data[field.id] = field.value or field.placeholder

            ConfigParser.addNewConnection(connection_data)
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

    @on(Select.Changed)
    def select_new_connection_type(self, event: Select.Changed):
        form = self.query_one(ConnectionForms)
        form.changeForm(event.value)
