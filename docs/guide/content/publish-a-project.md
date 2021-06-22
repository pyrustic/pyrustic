[Home](https://github.com/pyrustic/pyrustic#readme) | [Tutorial](https://github.com/pyrustic/pyrustic/blob/master/docs/tutorial/README.md) | [Guide](https://github.com/pyrustic/pyrustic/blob/master/docs/guide/README.md) | [Reference](https://github.com/pyrustic/pyrustic/blob/master/docs/reference/README.md) | [Website](https://pyrustic.github.io)

## Publish a project

Issue the command `publish` in `Project Manager`.

- you will be asked to submit your Github [personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token);
- then the `ante_release_hook.py` script will be executed;
- `$APP_DIR/pyrustic_data/release_info.json` will be edited by the previous script  
- `Project Manager` will read `release_info.json` then publish the latest distribution package ;
- `build_report.json` will be edited to confirm the successful release;
- then the `post_release_hook.py` script will be executed.

Study the scripts in the `$APP_PKG.hooking` package to understand what they do. You can edit them if you know what you are doing.

The command `publish` creates a release on Github then upload the distribution package as an asset.

If you don't want `Project Manager` to upload the latest distribution package, you can set `upload_asset` to `False` in `$APP_DIR/pyrustic_data/release_info.json`.
