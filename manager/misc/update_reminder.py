import os.path
from common import constants
import random
import time
from pyrustic.jasonix import Jasonix


class UpdateReminder:
    def __init__(self):
        pass

    def get_text(self):
        text = ""
        if not os.path.exists(constants.MANAGER_SHARED_DATA_FILE):
            return text
        one_week_in_seconds = 60 * 60 * 24 * 7
        two_weeks_in_seconds = one_week_in_seconds * 2
        three_weeks_in_seconds = one_week_in_seconds * 3
        random_time_in_future = random.randint(two_weeks_in_seconds, three_weeks_in_seconds)
        random_time_in_future = int(time.time()) + random_time_in_future
        jasonix = Jasonix(constants.MANAGER_SHARED_DATA_FILE)
        data = jasonix.data.get("update_reminder", None)
        if not data:
            jasonix.data["update_reminder"] = random_time_in_future
            jasonix.save()
            return text
        if int(time.time()) < data:
            return text
        jasonix.data["update_reminder"] = random_time_in_future
        jasonix.save()
        text = self._text()
        return text

    def _text(self):
        text = "\n\n\tHello Friend !"
        text += "\n\tYou can update Pyrustic Suite"
        text += "\n\twith the command 'update'."
        text += "\n\tThis is just a reminder."
        text += "\n\tEnjoy your programming journey !\n\n"
        return text
