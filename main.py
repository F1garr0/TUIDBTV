from textual.app import App, ComposeResult
import os
from textual.containers import *
from textual.widgets import Tree, DataTable, Footer

from controllers.PostgresController import PostgresController
from widgets.QuitScreen import QuitScreen
from widgets.SelectConnection import SelectConnection
from widgets.NewConnection import NewConnection

'''
TODO:
- add more connection types
- research jdbc analog
- add editor
- sort tables alphabetical
- add views preview
- add test connection button
- do not stop app if cannot connect
'''
# ---------------------------------------------------------------------------------------------

class TreeApp(App):
    CSS_PATH = "default.css"

    BINDINGS = [
        ("q", "quit_window()", "Quit"),
        ("s", "select_connection_window()", "Select connection"),
        ("n", "new_connection_window()", "New Connection"),
    ]

    def compose(self) -> ComposeResult:

        with Horizontal():
            yield Tree("schemas")
            yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        def select_connection(data):
            self.dbController = PostgresController(data['database'], data['userName'], data['password'], data['hostName'], data['port'])
            tree = self.query_one(Tree)
            tree.root.expand()
            for schemaName in self.dbController.getSchemaNames():
                schema = tree.root.add(schemaName[0])
                for tableName in self.dbController.getTableNamesBySchema(schemaName[0]):
                    schema.add_leaf(tableName[0])

        self.push_screen(SelectConnection(_can_quit=False), select_connection)

    def on_tree_node_selected(self, event):
        if not event.node.children:
            table = self.query_one(DataTable)
            table.clear(columns=True)
            tableData = self.dbController.getTablePreview(event.node.parent.label, event.node.label)
            table.add_columns(*tableData[0])
            table.zebra_stripes = True
            table.add_rows(tableData[1:])

    def action_quit_window(self):
        self.push_screen(QuitScreen())

    def action_select_connection_window(self):
        self.push_screen(SelectConnection())

    def action_new_connection_window(self):
        self.push_screen(NewConnection())

# ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    app = TreeApp()
    reply = app.run()
    print(reply)
