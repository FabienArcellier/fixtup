#!/bin/bash
#
# github action invoke this script in the workflow validate_examples
# to check this example in the continuous integration process
# of fixtup.

python3 -m unittest discover tests/integrations
