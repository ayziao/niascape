#!/bin/bash
PROJECT_DIR=$(cd $(dirname $0)/..;pwd)
cd ${PROJECT_DIR}
rm -r htmlcov
if [ $1 = pypy ]; then
  pypy3 -m coverage run --branch --source=niascape tests
else
  coverage run --branch --source=niascape tests
fi
coverage report -m 
coverage html --title="Coverage report $1"  && open -a "Google Chrome" file://${PROJECT_DIR}/htmlcov/index.html
cd htmlcov
find . -type f -name "*.html" -print0 | xargs -0 sed -i -e "s/        /  /g"
