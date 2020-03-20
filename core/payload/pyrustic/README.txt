This package is the heart of the framework.
It will be replaced during an update/upgrade (check the command 'sync' in Pyrustic Platform Shell).
It is therefore strongly recommended not to alter its content otherwise you will lose your modifications during an update.

It should be noted that during an update, the package is cached in "cache/rollback".
Another update will overwrite "cache/rollback".

Example: your project currently uses pyrustic 0.0.1 build 1
You decide to update to build 12.
In this case, build 1 is automatically cached in "cache/rollback" and build 12 is installed.
The next time you install for example build 15, build 12 will be cached in "cache/rollback" by overwriting the previous one.
