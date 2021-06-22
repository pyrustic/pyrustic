[Home](https://github.com/pyrustic/pyrustic#readme) | [Tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md) | [Guide](https://github.com/pyrustic/pyrustic/blob/master/docs/guide/README.md) | [Reference](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md) | [Website](https://pyrustic.github.io)

## Build a project

Issue the command `build` in `Project Manager`.

- you will be asked if you want to run tests;
- the versioning mechanism will take the control;
- then the `ante_build_hook.py` script will be executed;
- `Project Manager` will build a distribution package (Wheel);
- a `build_report.json` will be generated in `$APP_DIR/pyrustic_data`;
- then the `post_build_hook.py` script will be executed.

Study the scripts in the `$APP_PKG.hooking` package to understand what they do. You can edit them if you know what you are doing.
