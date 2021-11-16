"""This module runs the tests located in the package tests"""
import os
from backstage import api


project_dir = os.getcwd()
tests_success, tests_result = api.run_tests(project_dir)
if tests_success is True:
    print("Testing passed !\n")
elif tests_success is False:
    print("Testing failed !\n")
    print(tests_result)
else:
    print("No tests available.")
