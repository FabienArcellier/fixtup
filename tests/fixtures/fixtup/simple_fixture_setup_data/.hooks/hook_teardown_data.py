#!/usr/bin/env python
#
# rename this file into hook_teardown_data.py to activate
# this hook.
#
# this hook is executed after each test
#
# This hook is executed between each test and is intended
# to clean dataset in a database or another system before moving to the next test.
import os

os.remove(os.path.join(os.getcwd(), 'file.data'))
