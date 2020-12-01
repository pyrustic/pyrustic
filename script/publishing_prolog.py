import sys
import about
import os.path
from pyrustic.jasonix import Jasonix
from pyrustic import pymisc


EXIT_CODE = 0
SCRIPT_PATH = sys.argv[0]
CACHED_TARGET_ROOT = sys.argv[1]
TOKEN = sys.argv[2]
PUBLISHING_FORM_PATH = sys.argv[3]

# Write your code here
cached_target_about_json = os.path.join(CACHED_TARGET_ROOT,
                                 "pyrustic_data",
                                 "about.json")
jasonix = Jasonix(cached_target_about_json)
jasonix.data["dev_mode"] = False
jasonix.save()

# Exiting this script
sys.exit(EXIT_CODE)
