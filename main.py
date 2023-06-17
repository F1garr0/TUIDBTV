from textual import on
from textual.app import App, ComposeResult
import os
from textual.containers import *
from textual.suggester import SuggestFromList
from textual.widgets import Tree, DataTable, Footer, Header, TabbedContent, TabPane, Markdown, TextLog, Input, Button

from widgets.PopUpScreen import PopUpScreen
from widgets.QuitScreen import QuitScreen
from widgets.SelectConnection import SelectConnection
from widgets.NewConnection import NewConnection

sql_abc = ["select rolname from pg_catalog.pg_roles;"]

'''
TODO:
- add more connection types
- research jdbc analog
- sort tables alphabetical
- add views preview
- add edit connection functionality
'''


# ---------------------------------------------------------------------------------------------

class TUIDBTV(App):
    CSS_PATH = "default.css"

    BINDINGS = [
        ("q", "quit_window()", "Quit"),
        ("s", "select_connection_window()", "Select connection"),
        ("n", "new_connection_window()", "New Connection"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree("schemas")
            with TabbedContent():
                with TabPane("preview", id="preview_tab"):
                    yield DataTable(id="preview_data_table")
                with TabPane("editor", id="editor_tab"):
                    yield Input(suggester=SuggestFromList(sql_abc, case_sensitive=False), id="new_request_input")
                    yield Button("Run", id="execute_editor_button")
                    yield DataTable(id="editor_table")
                with TabPane("+", id="add_new_tab"):
                    yield Markdown()
        yield Footer()

    def on_mount(self) -> None:
        def select_connection(db_contoller):
            self.dbController = db_contoller
            tree = self.query_one(Tree)
            tree.root.expand()
            for schemaName in self.dbController.getSchemaNames():
                schema = tree.root.add(schemaName[0])
                for tableName in self.dbController.getTableNamesBySchema(schemaName[0]):
                    schema.add_leaf(tableName[0])

        self.push_screen(SelectConnection(_can_quit=False), select_connection)

    def on_tree_node_selected(self, event):
        if not event.node.children:
            table = self.query_one("#preview_data_table")
            table.clear(columns=True)
            tableData = self.dbController.getTablePreview(event.node.parent.label, event.node.label)
            table.add_columns(*tableData[0])
            table.zebra_stripes = True
            table.add_rows(tableData[1:])

    @on(Button.Pressed)
    def execute_editor_query(self, event: Button.Pressed):
        if event.button.id == "execute_editor_button":
            query_text = self.query_one("#new_request_input", expect_type=Input).value
            try:
                data = self.dbController.executyQueryWithHeaders(query_text)
                table = self.query_one("#editor_table")
                table.clear(columns=True)
                table.add_columns(*data[0])
                table.zebra_stripes = True
                table.add_rows(data[1:])
            except:
                self.push_screen(PopUpScreen("Error :c"))

    def action_quit_window(self):
        self.push_screen(QuitScreen())

    def action_select_connection_window(self):
        self.push_screen(SelectConnection())

    def action_new_connection_window(self):
        self.push_screen(NewConnection())


# ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    app = TUIDBTV()
    reply = app.run()
    print(reply)
