class TutorialCatalog:


    TEXT_INTRO = """
    Welcome to Pyrustic !
    
    
    INTRODUCTION
    ============
    
    Pyrustic is a lightweight software suite for developing
    your next Python desktop application.
    
    Pyrustic is built with Python and uses the same framework
    that will support your next project.
    This project is under a free and permissive license.

    The first concrete element is the Manager, 
    soberly titled 'Pyrustic Manager'.
    
    This tutorial is currently displayed in the Manager.
    
    As the name already suggests, Pyrustic Manager
    takes care of managing the 'target project' among others.
    The "target project" is the project you want to
    build with Pyrustic.
    
    The Manager allows you to create your target project,
    add modules, packages, etc.
    
    When you create your target project with the manager,
    Pyrustic Framework is installed automatically in
    the target project.
    Pyrustic Framework comes with widgets (megawidgets to be precise),
    a very practical theme/style system, a gateway to elegantly
    communicate with the database, a tool for performing multithreading
    properly, etc.
    
    As you develop your project, you will need a database editor
    and a test runner. These tools are accessible in the Manager
    and are by default configured to run in the context of your project.
    Yes, integration !
    
    Pyrustic is a project that has just started, the documentation
    will be precarious and all versions below version 1.0.0 will be
    considered to be Beta at best.
    
    A demo is included to allow you to study it and learn quickly.
    
    
    HOW TO BUILD YOUR PROJECT
    =========================
    
    To create your project, start the Manager and use the Target
    command as follows:
    
    >>> target path_to_project_directory
    
    Your project directory would therefore already be created upstream. 
    
    If your project directory is empty, the Manager will install 
    the standard folders and files there and then add 
    the optional folders and files: 'view', 'host', 'misc', 'dao',
    'script.py' and 'config.ini'.
    
    If your project folder is not empty, then the Manager will
    assume that you have already your own project structure, 
    and therefore the Manager will only install there the 
    standard files and folders.
    
    Manager saves the last Target, so the next time you open
    the Manager, you just have to enter the command 'target'
    without parameters to reload the last Target.
    
    
    DESCRIPTION OF A TYPICAL PROJECT
    ================================
    
    The entry point for your project (Target) is the 'main.py' file.
    
    In the 'main.py' file, you must instantiate the pyrustic.app.App
    class and then link it the instance of the first View of the project. 
    
    A View is a class that you build to
    manages the GUI part of your project. A View must subclass
    'pyrustic.abstract.viewable.Viewable' and implement the methods:
    '_on_build()', '_on_display()' and '_on_destroy()'.
    
    All views must have an instance variable '_body'. 
    This variable must contain the widget to display at
    the screen.
    
    To build a View, you have to call its 'build()' method
    which returns its 'body'.
    
    A view object also has a 'body' property.
    
    To destroy a View, you can use its 'destroy()' method.
    
    The lifecycle of a View is as follows: 
    by calling the method 'build()', '_on_build()' is implicitly 
    executed, then once the View is visible on the screen,
    '_on_display()' is executed, then finally '_on_destroy()'
    is executed when the application is going to shutdown or 
    when the View is destroyed.
    
    
    CONCLUSION
    ===========
    
    Pyrustic is still in its infancy, a demo is included 
    to help you to understand by example.
    
    To create the demo, use the demo command in the Manager:
    
    >>> demo path_to_empty_directory
    
    Then set the demo path as target, so you could play with the commands
    'test', 'dbase' and 'run' in the manager. 
    
    Of course you can execute the demo traditionally outside the Manager,
    just launch the file 'main.py'.
    
    Good luck dear early adopter !
    And thanks you for your intellectual curiosity !
    It is a rare quality nowadays !
    And don't forget that lots of good things are yet to come !
    
    
    P.S: feel free to contribute: https://github.com/pyrustic
    
    
    
    ~ Pyrustic Evangelist ~
    
    """
