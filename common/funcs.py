from common import constants
from pyrustic.jasonix import Jasonix


def get_manager_jasonix(readonly=True):
    jasonix = Jasonix(constants.MANAGER_SHARED_DATA_FILE,
                        constants.DEFAULT_MANAGER_SHARED_DATA_FILE,
                        readonly)
    return jasonix


def get_sqleditor_jasonix(readonly=True):
    jasonix = Jasonix(constants.SQLEDITOR_SHARED_DATA_FILE,
                        constants.DEFAULT_SQLEDITOR_SHARED_DATA_FILE,
                        readonly)
    return jasonix


def get_runtest_jasonix(readonly=True):
    jasonix = Jasonix(constants.RUNTEST_SHARED_DATA_FILE,
                        constants.DEFAULT_RUNTEST_SHARED_DATA_FILE,
                        readonly)
    return jasonix


def get_hub_jasonix(readonly=True):
    jasonix = Jasonix(constants.HUB_SHARED_DATA_FILE,
                        constants.DEFAULT_HUB_SHARED_DATA_FILE,
                        readonly)
    return jasonix


def get_hub_url(res):
    target = "https://api.github.com"
    return "{}{}".format(target, res)
