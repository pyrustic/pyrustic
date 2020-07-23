from pyrustic.app import App
import about
import sys
import os.path
from tool.runtest.misc.builder import MainViewBuilder
from tool.runtest.theme import RUNTEST_THEME


app = App()
app.root.title("Pyrustic Test Runner")
app.theme = RUNTEST_THEME
app.config = os.path.join(about.ROOT_DIR, "tool", "runtest", "config.ini")
app.view = MainViewBuilder().build(app.root)
app.start()
