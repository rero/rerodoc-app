#! /bin/bash

npm i -g --prefix $VIRTUAL_ENV npm
npm install --prefix $VIRTUAL_ENV -g node-sass clean-css clean-css-cli requirejs uglify-js
pip install -r $VIRTUAL_ENV/src/rerodoc-app/requirements-devel.txt
pip install -e $VIRTUAL_ENV/src/rerodoc-app/[all]
invenio collect -v
invenio npm

cd $VIRTUAL_ENV/var/instance/static
npm i
cd -
invenio assets build

cp $VIRTUAL_ENV/src/rerodoc-app/development/scripts/{install.sh,populate.sh,postactivate,predeactivate} $VIRTUAL_ENV/bin
