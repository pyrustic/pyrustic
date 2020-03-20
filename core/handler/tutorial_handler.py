
class TutorialHandler:
    """
    To create a new project, use the 'make' command.

    If the project name is "my_project" and you want to create it in the directory "/user/me",
    make sure that there is no folder named "my_project" in the directory.
    Meaning: "/user/me/my_project" doesn't exist prior to the project creation.

    Once the project is created, its path is saved and therefore becomes the "target".
    Use the "target" command to find out which project is targeted (it shows some extra information) 
    Note that you can use the same command "target" to target another project that already exists.

    To create a new dao, or host, or view, or misc file, please refer to the "dao",
    "host", "view", and "misc" commands respectively.
    If you don't understand yet what is "dao, host, view...", read the file:
        "what_is_pyrustic_framework.text" (located in the root of Pyrustic Platform Shell).

    You can create a new package in your project with the "package" command.
    This package "my.fake.long.useless.boring.secret.dirty.deep.package" can be created
    easily with the commande "package". Yes, "__init__.py" will be inside each sub-package.

    It is also possible to import a file into your project using the "import" command.
    It could be useful... someday... for something...

    The "feed" command is to be used when you want to update the Pyrustic Platform Shell.
    Note that you can feed the platform with old zipped versions too.
    When you feed the platform with a zipped new version, this version is stored in "archive".
    If the version is new, it will be installed.

    To find out the version of Pyrustic Platform Shell, use the "version" command.
    This command will show the list of available versions too (the ones in the "archive").

    The "switch" command allows you to change the current version of Pyrustic Platform Shell
    provided that there is another version in the archive.

    The "sync" command allows you to synchronize the Pyrustic version of "target" (your project)
    with the current version of Pyrustic Platform Shell.
    Meaning: update the framework of your project with this command.

    When the platform changes current version, the old one is cached in the "rollback"
    folder which is created in the "cache" folder of Pyrustic Plaftorm Shell

    That's all for the moment.
    """
