from pyrustic.app import App
import os.path
from pyrustic import about as pyrustic_about
from pyrustic.private.tool.sqleditor.misc.builder import MainViewBuilder
from pyrustic.private.tool.sqleditor.misc import my_theme


app = App()
app.root.title("Pyrustic SQL Editor")
app.config = os.path.join(pyrustic_about.ROOT_DIR, "private",
                          "tool", "sqleditor", "config.json")
app.theme = my_theme.get_theme()
app.view = MainViewBuilder().build(app)
app.center()
app.start()
