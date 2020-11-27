import about
import os.path
from pyrustic.app import App
from hub.misc import my_theme
from hub.view.main_view import MainView


app = App()
app.root.title("Pyrustic Hub")
app.config = os.path.join("hub", "config.json")
app.theme = my_theme.get_theme()
app.view = MainView(app)
app.start()
