from misc.tutorial_catalog import TutorialCatalog

class TutorialHandler:
    def __init__(self, args):
        self._process(args)

    def _process(self, args):
        if not args:
            self._print_intro()

    def _print_intro(self):
        print(TutorialCatalog.TEXT_INTRO)
