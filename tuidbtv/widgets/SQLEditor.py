from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Button, DataTable

from tuidbtv.suggesters.SuggesterDict import SuggesterDict
from tuidbtv.widgets.PopUpScreen import PopUpScreen

sql_abc = ["select", "from", "where", "join", "right", "left", "inner", "like", "insert", "into", "update",
           "order", "group", "by", "as", "on"]


class SQLEditor(Widget):
    def compose(self) -> ComposeResult:
        yield Input(suggester=SuggesterDict(sql_abc, case_sensitive=False), id="new_request_input")
        yield Button("Run", id="execute_editor_button")
        yield DataTable(id="editor_table")

    @on(Button.Pressed)
    def execute_editor_query(self, event: Button.Pressed):
        if event.button.id == "execute_editor_button":
            query_text = self.query_one("#new_request_input", expect_type=Input).value
            try:
                data = self.app.dbController.executeQueryWithHeaders(query_text)
                table = self.query_one("#editor_table")
                table.clear(columns=True)
                table.add_columns(*data[0])
                table.zebra_stripes = True
                table.add_rows(data[1:])
            except Exception as e:
                self.app.push_screen(PopUpScreen(e.__str__()))
