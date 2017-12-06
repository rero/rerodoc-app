#! /bin/bash

FLASK_DEBUG=0
INVENIO_OAIHARVESTER_WORKDIR=$VIRTUAL_ENV/src/rerodoc-app/data
invenio oaiharvester harvest -d postprints -m marcxml -u http://doc.rero.ch/oai2d -s postprint -f 2017-01-01 -k
