import os.path
from pyrustic.app import App
from pyrustic import about as pyrustic_about
from pyrustic.private.tool.hub.misc import my_theme
from pyrustic.private.tool.hub.view.main_view import MainView


app = App()
app.root.title("Pyrustic Hub")
app.config = os.path.join(pyrustic_about.ROOT_DIR, "private",
                          "tool", "hub", "config.json")
app.theme = my_theme.get_theme()
app.view = MainView(app)
app.center()
app.start()
