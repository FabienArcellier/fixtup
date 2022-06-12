#!/usr/bin/env python
#
# rename this file into hook_setup_data.py to activate
# this hook.
#
# this hook is executed before every test
#
# This hook is executed between each test and is intended
# to mount a dataset in a database or another system before playing the test.
import os
import io

with io.open(os.path.join(os.getcwd(), 'file.data'), "w+") as fp:
    fp.write("hello world")
