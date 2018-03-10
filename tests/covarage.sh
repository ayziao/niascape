#!/bin/bash
PROJECT_DIR=$(cd $(dirname $0)/..;pwd)
cd $PROJECT_DIR
coverage run --branch --source=niascape tests
coverage report -m 
coverage html && open -a "Google Chrome" file://$PROJECT_DIR/htmlcov/index.html
