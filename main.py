import os
from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Tree, DataTable, Footer, Header, TabbedContent, TabPane, Markdown, TextLog, Input, Button

from widgets.QuitScreen import QuitScreen
from widgets.SQLEditor import SQLEditor
from widgets.SelectConnection import SelectConnection

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
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree("schemas")
            with TabbedContent():
                with TabPane("preview", id="preview_tab"):
                    yield DataTable(id="preview_data_table")
                with TabPane("editor", id="editor_tab"):
                    yield SQLEditor()
                with TabPane("+", id="add_new_tab"):
                    yield Markdown()
        yield Footer()

    def openConnectionSelectScreen(self):
        def select_connection(db_controller):
            self.dbController = db_controller
            tree = self.query_one(Tree)
            tree.root.expand()
            for schemaName in self.dbController.getSchemaNames():
                schema = tree.root.add(schemaName[0])
                for tableName in self.dbController.getTableNamesBySchema(schemaName[0]):
                    schema.add_leaf(tableName[0])

        self.push_screen(SelectConnection(_can_quit=False), select_connection)

    def on_mount(self) -> None:
        self.openConnectionSelectScreen()

    def on_tree_node_selected(self, event):
        if not event.node.children:
            table = self.query_one("#preview_data_table")
            table.clear(columns=True)
            tableData = self.dbController.getTablePreview(event.node.parent.label, event.node.label)
            table.add_columns(*tableData[0])
            table.zebra_stripes = True
            table.add_rows(tableData[1:])

    def action_quit_window(self):
        self.push_screen(QuitScreen())

    def action_select_connection_window(self):
        tree = self.query_one(Tree)
        tree.clear()
        self.openConnectionSelectScreen()

# ---------------------------------------------------------------------------------------------


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    app = TUIDBTV()
    reply = app.run()
    print(reply)
