#!/bin/bash
PROJECT_DIR=$(cd $(dirname $0)/..;pwd)
cd ${PROJECT_DIR}
rm -r htmlcov
OPTION=$1
if [ ${OPTION} = "pypy" ] ; then
  pypy3 -m coverage run --branch --source=niascape tests
elif [ ${OPTION} = "all" ] ; then
  coverage run --branch --source=niascape tests
  pypy3 -m coverage run -a --branch --source=niascape tests
else
  coverage run --branch --source=niascape tests
fi
coverage report -m 
coverage html --title="Coverage report ${OPTION}"  && open -a "Google Chrome" file://${PROJECT_DIR}/htmlcov/index.html
cd htmlcov
find . -type f -name "*.html" -print0 | xargs -0 sed -i -e "s/        /  /g"
