from pyrustic.app import App
import about
import os.path
from sqleditor.misc.builder import MainViewBuilder
from sqleditor.misc import my_theme


app = App()
app.root.title("Pyrustic SQL Editor")
app.config = os.path.join("sqleditor", "config.json")
app.theme = my_theme.get_theme()
app.view = MainViewBuilder().build(app)
app.start()
