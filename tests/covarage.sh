#!/bin/bash
PROJECT_DIR=$(cd $(dirname $0)/..;pwd)
cd ${PROJECT_DIR}
rm -r htmlcov
coverage run --branch --source=niascape tests
coverage report -m 
coverage html && open -a "Google Chrome" file://${PROJECT_DIR}/htmlcov/index.html
cd htmlcov
find . -type f -name "*.html" -print0 | xargs -0 sed -i -e "s/        /  /g"
