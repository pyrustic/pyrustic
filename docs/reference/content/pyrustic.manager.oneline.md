
Back to [Reference Overview](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md)

# pyrustic.manager.oneline



<br>


```python
HANDLERS = {'add': <class 'pyrustic.manager.handler.add_handler.AddHandler'>, 'build': <class 'pyrustic.manager.handler.build_handler.BuildHandler'>, 'hub': <class 'pyrustic.manager.handler.hub_handler.HubHandler'>, 'init': <class 'pyrustic.manager.handler.init_handler.InitHandler'>, 'link': <class 'pyrustic.manager.handler.link_handler.LinkHandler'>, 'publish': <class 'pyrustic.manager.handler.publish_handler.PublishHandler'>, 'recent': <class 'pyrustic.manager.handler.recent_handler.RecentHandler'>, 'relink': <class 'pyrustic.manager.handler.relink_handler.RelinkHandler'>, 'run': <class 'pyrustic.manager.handler.run_handler.RunHandler'>, 'target': <class 'pyrustic.manager.handler.target_handler.TargetHandler'>, 'unlink': <class 'pyrustic.manager.handler.unlink_handler.UnlinkHandler'>, 'version': <class 'pyrustic.manager.handler.version_handler.VersionHandler'>}

```

<br>

```python

def command(line=None, target=None):
    """
    Param:
        - line is a string or a list. Example "link /home/project" or ["link", "/home/proj"]
        - target is a path string
    """

```

