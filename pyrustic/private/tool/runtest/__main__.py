from pyrustic.app import App
import os.path
from pyrustic import about as pyrustic_about
from pyrustic.private.tool.runtest.misc.builder import MainViewBuilder
from pyrustic.private.tool.runtest.misc import my_theme


app = App()
app.root.title("Pyrustic Test Runner")
app.config = os.path.join(pyrustic_about.ROOT_DIR, "private",
                          "tool", "runtest", "config.json")
app.theme = my_theme.get_theme()
app.view = MainViewBuilder().build(app)
app.center()
app.start()
