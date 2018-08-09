#! /bin/bash

npm i -g --prefix $VIRTUAL_ENV npm
npm update && npm install --prefix $VIRTUAL_ENV --silent -g node-sass@4.9.0 clean-css@3.4.19 uglify-js@2.7.3 requirejs@2.2.0

pip install -r $VIRTUAL_ENV/src/rerodoc-app/requirements-devel.txt
pip install -e $VIRTUAL_ENV/src/rerodoc-app/[all]
invenio collect -v
invenio npm

cd $VIRTUAL_ENV/var/instance/static
npm i
cd -
invenio assets build

cp $VIRTUAL_ENV/src/rerodoc-app/development/scripts/{install.sh,populate.sh,postactivate,predeactivate} $VIRTUAL_ENV/bin
