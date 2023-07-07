from textual import on
from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Tree, DataTable, Footer, Header, TabbedContent, TabPane, Markdown, ContentSwitcher

from tuidbtv.widgets.QuitScreen import QuitScreen
from tuidbtv.widgets.SQLEditor import SQLEditor
from tuidbtv.widgets.SelectConnection import SelectConnection

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
        ("r", "quit_window()", "Refresh"),
        ("a", "add_new_tab()", "Add tab"),
        ("d", "remove_current_tab()", "Delete current tab"),
    ]

    def __init__(self):
        super().__init__()
        self.tabs_count = 0
        self.suggestions = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree("schemas")
            with TabbedContent():
                with TabPane("preview", id="preview_tab"):
                    yield DataTable(id="preview_data_table")
                with TabPane("editor", id="editor_tab"):
                    yield SQLEditor()
                with TabPane(" + ", id="add_new_tab_pane"):
                    yield Markdown()
        yield Footer()

    def openConnectionSelectScreen(self, _firstRun = False):
        def select_connection(db_controller):
            self.dbController = db_controller
            tree = self.query_one(Tree)
            tree.clear()
            tree.root.expand()
            self.suggestions = []
            for schemaName in self.dbController.getSchemaNames():
                schema = tree.root.add(schemaName[0])
                self.suggestions.append(schemaName[0])
                for tableName in self.dbController.getTableNamesBySchema(schemaName[0]):
                    schema.add_leaf(tableName[0])
                    self.suggestions.append(tableName[0])
                    self.suggestions.append(f"{schemaName[0]}.{tableName[0]}")
            for editor in self.query(SQLEditor).nodes:
                editor.clean_completions()
                editor.add_completions(self.suggestions)

        self.push_screen(SelectConnection(firstRun=_firstRun), select_connection)

    def on_mount(self) -> None:
        self.openConnectionSelectScreen(_firstRun=True)

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        if not event.node.allow_expand:
            table = self.query_one("#preview_data_table")
            table.clear(columns=True)
            tableData = self.dbController.getTablePreview(event.node.parent.label, event.node.label)
            table.add_columns(*tableData[0])
            table.zebra_stripes = True
            table.add_rows(tableData[1:])

    def action_quit_window(self):
        self.push_screen(QuitScreen())

    def action_select_connection_window(self):
        self.openConnectionSelectScreen()

    def action_add_new_tab(self):
        tab_pane = self.query_one(TabbedContent)
        add_new_tab_pane = self.query("#add_new_tab_pane").filter("TabPane").first()
        self.tabs_count += 1
        new_tab_id = f"editor_tab{self.tabs_count}"
        tab_pane.add_pane(
            TabPane(new_tab_id, SQLEditor(self.suggestions), id=new_tab_id),
            before = add_new_tab_pane
        )
        return new_tab_id

    def action_remove_current_tab(self):
        tab_pane = self.query_one(TabbedContent)
        active_tab_id = tab_pane.active
        if active_tab_id not in ["preview_tab", "editor_tab", "add_new_tab_pane"]:
            tab_pane.remove_pane(active_tab_id)

    @on(TabbedContent.TabActivated)
    def add_new_tab_opened(self, event: TabbedContent.TabActivated):
        if event.tab.label.__str__() == " + ":
            new_tab_id = self.action_add_new_tab()
            tab_pane = self.query_one(TabbedContent)
            switcher = tab_pane.get_child_by_type(ContentSwitcher)
            tab_pane.active = new_tab_id
            switcher.current = new_tab_id


# ---------------------------------------------------------------------------------------------

def run():
    # os.environ['TERM'] = 'xterm-256color'
    app = TUIDBTV()
    reply = app.run()
    print(reply)


if __name__ == "__main__":
    run()
