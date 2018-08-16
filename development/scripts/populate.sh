#! /bin/bash

FLASK_DEBUG=0

invenio db destroy --yes-i-know || true
invenio index destroy --force --yes-i-know || true

invenio db init create
invenio index init

# remove useless indexes
invenio index delete --force --yes-i-know marc21-bibliographic-bd-v1.0.0 || true
invenio index delete --force --yes-i-know circulation-item-default-v1.0.0 || true
invenio index delete --force --yes-i-know marc21-authority-ad-v1.0.0 || true
invenio index delete --force --yes-i-know marc21-holdings-hd-v1.0.0 || true

invenio index queue init
invenio utils alias records iheid

echo "Creating accounts..."
# create new user
invenio users create -a admin@rero.ch --password administrator
invenio users create -a librarian@rero.ch --password librarian

# create roles
invenio roles create -d "Admins Group" admins
invenio roles create -d "Super Users Group" superusers
invenio roles create -d "Cataloguer" cataloguer

# grant accesses to action roles
invenio access allow admin-access role admins
invenio access allow superuser-access role superusers

# grant roles to users
invenio roles add admin@rero.ch admins
invenio roles add admin@rero.ch superusers
invenio roles add librarian@rero.ch cataloguer

invenio collections create rerodoc

echo "Creating document type collections..."
invenio collections create -p rerodoc type
invenio collections create -p type -q "type.main:book" type.book

echo "Creating institution collections..."
invenio collections create -p rerodoc institution
invenio collections create -p institution institution.fribourg
invenio collections create -p institution.fribourg -q "institution:bcufr" institution.fribourg.bucfr
invenio collections create -p institution institution.valais
invenio collections create -p institution.valais -q "institution:medvs" institution.valais.medvs
invenio collections create -p institution institution.neuchatel_jura
invenio collections create -p institution.neuchatel_jura -q "institution:bicj" institution.neuchatel_jura.bicj
invenio collections create -p institution.neuchatel_jura -q "institution:pbune" institution.neuchatel_jura.bpune
invenio collections create -p institution institution.geneve
invenio collections create -p institution.geneve -q "institution:baage" institution.geneve.baage
invenio collections create -p institution.geneve -q "institution:bpuge" institution.geneve.bpuge
invenio collections create -p institution.geneve -q "institution:iheid" institution.geneve.iheid
invenio collections create -p institution.geneve -q "institution:imvge" institution.geneve.imvge

echo "creating udc collections..."
invenio collections create -p rerodoc udc
invenio collections create -p udc udc.sciences_exactes_et_naturelles
invenio collections create -p udc.sciences_exactes_et_naturelles udc.sciences_exactes_et_naturelles.sciences_de_la_terre
invenio collections create -p udc.sciences_exactes_et_naturelles.sciences_de_la_terre udc.sciences_exactes_et_naturelles.sciences_de_la_terre.geologie
invenio collections create -q "udc:56" -p udc.sciences_exactes_et_naturelles.sciences_de_la_terre.geologie udc.sciences_exactes_et_naturelles.sciences_de_la_terre.geologie.paleontologie

echo "Creating specific collections..."
invenio collections create -p rerodoc specific_collection
invenio collections create -p specific_collection specific_collection.geneve
invenio collections create -q 'specific_collection:"BAA - Bibliographie Hodler"' -p specific_collection.geneve specific_collection.geneve.bibliographie_holder

# harvest articles and books on the production server
#invenio oaiharvester harvest --signals -u http://doc.rero.ch/oai2d -s "book" -d oia -m marcxml -k -e 'utf-8'
echo "Load data..."
# invenio utils load $VIRTUAL_ENV/src/rerodoc-app/data/full_book.json

#dojson -i $VIRTUAL_ENV/src/rerodoc-app/data/book.xml -l marcxml do book schema http://rerodoc.test.rero.ch/schema/records/book-v0.0.1.json|invenio utils load -m 100 --skip --no-files
#dojson -i data/book.xml -l marcxml do book schema http://rerodoc.test.rero.ch/schema/records/book-v0.0.1.json|invenio utils load --skip

# invenio index run
#invenio index run -d -c 10
# For data correction
#dojson -i data/book.xml -l marcxml do book schema http://rerodoc.test.rero.ch/schema/records/book-v0.0.1.json|invenio utils load -vvv -m 500 --no-files
