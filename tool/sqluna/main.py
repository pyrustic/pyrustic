from pyrustic.app import App
import about
import os.path
from tool.sqluna.misc.builder import MainViewBuilder
from tool.sqluna.theme import SQLUNA_THEME


app = App()
app.root.title("Pyrustic Database Editor")
app.theme = SQLUNA_THEME
app.config = os.path.join(about.ROOT_DIR, "tool", "sqluna", "config.ini")
app.view = MainViewBuilder().build(app)
app.start()
