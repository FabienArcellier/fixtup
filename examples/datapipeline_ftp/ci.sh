#!/bin/bash
#
# github action invoke this script in the workflow validate_examples
# to check this example in the continuous integration process
# of fixtup.


poetry run pytest tests/integrations
