#! /bin/bash

npm install --prefix $VIRTUAL_ENV -g node-sass clean-css clean-css-cli requirejs uglify-js
pip install -r requirements-devel.txt
pip install -e .[all]
invenio collect -v
invenio npm

cd $VIRTUAL_ENV/var/instance/static
npm i
cd -
invenio assets build
