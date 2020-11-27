from pyrustic.app import App
import about
import os.path
from runtest.misc.builder import MainViewBuilder
from runtest.misc import my_theme


app = App()
app.root.title("Pyrustic Test Runner")
app.config = os.path.join("runtest", "config.json")
app.theme = my_theme.get_theme()
app.view = MainViewBuilder().build(app)
app.start()
from pathlib import Path