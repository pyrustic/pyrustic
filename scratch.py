from pyrustic.app import App
from pyrustic.widget.choice import Choice
from hub.misc import my_theme

app = App()
app.theme = my_theme.get_theme()
app.view = Choice(app.root, message="MESSAGE", title="Title", header="Header",
                  items=["One", "Two", "Three", "Four"], use_scrollbox=True)
app.start()
