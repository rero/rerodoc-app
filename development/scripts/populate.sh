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

invenio collections create RERO_DOC
invenio collections create -p RERO_DOC RERO_DOC.NAVDOCTYPE
invenio collections create -p RERO_DOC.NAVDOCTYPE -q "document_type.main:book" RERO_DOC.NAVDOCTYPE.BOOK
invenio collections create -p RERO_DOC RERO_DOC.NAVSITE
invenio collections create -p RERO_DOC.NAVSITE RERO_DOC.NAVSITE.FRIBOURG
invenio collections create -p RERO_DOC.NAVSITE RERO_DOC.NAVSITE.VALAIS
invenio collections create -p RERO_DOC.NAVSITE RERO_DOC.NAVSITE.VAUD
invenio collections create -p RERO_DOC.NAVSITE RERO_DOC.NAVSITE.GENEVE
invenio collections create -p RERO_DOC.NAVSITE RERO_DOC.NAVSITE.NEUCHATEL
invenio collections create -p RERO_DOC.NAVSITE.VAUD -q "institution.code:CIO" RERO_DOC.NAVSITE.VAUD.CIO
invenio collections create -p RERO_DOC.NAVSITE.GENEVE -q "institution.code:BAAGE" RERO_DOC.NAVSITE.GENEVE.BAAGE
invenio collections create -p RERO_DOC.NAVSITE.VALAIS -q "institution.code:MEDVS" RERO_DOC.NAVSITE.VALAIS.MEDVS
invenio collections create -p RERO_DOC.NAVSITE.GENEVE -q "institution.code:BPUGE" RERO_DOC.NAVSITE.GENEVE.BPUGE
invenio collections create -p RERO_DOC.NAVSITE.GENEVE -q "institution.code:IHEID" RERO_DOC.NAVSITE.GENEVE.IHEID
invenio collections create -p RERO_DOC.NAVSITE.FRIBOURG -q "institution.code:BUCFR" RERO_DOC.NAVSITE.FRIBOURG.BUCFR
invenio collections create -p RERO_DOC.NAVSITE.NEUCHATEL -q "institution.code:BICJ" RERO_DOC.NAVSITE.NEUCHATEL.BICJ
invenio collections create -p RERO_DOC.NAVSITE.NEUCHATEL -q "institution.code:BPUNE" RERO_DOC.NAVSITE.NEUCHATEL.BPUNE
invenio collections create -p RERO_DOC.NAVSITE.GENEVE -q "institution.code:IMVGE" RERO_DOC.NAVSITE.GENEVE.IMVGE
invenio collections create -p RERO_DOC.NAVSITE.VAUD -q "institution.code:SAEF" RERO_DOC.NAVSITE.VAU${INVENIO_WEB_INSTANCE}
invenio collections create  -p RERO_DOC RERO_DOC.NAVDOM
invenio collections create  -p RERO_DOC.NAVDOM RERO_DOC.NAVDOM.LETTRES_SCIENCES_HUMAINES_ET_SOCIALES
invenio collections create -q "udc.code:796"  -p RERO_DOC.NAVDOM.LETTRES_SCIENCES_HUMAINES_ET_SOCIALES NAVDOM.LETTRES_SCIENCES_HUMAINES_ET_SOCIALES.SCIENCES_DU${INVENIO_WEB_INSTANCE}
invenio collections create -p RERO_DOC RERO_DOC.NAVCOLLSPEC
invenio collections create -p RERO_DOC.NAVCOLLSPEC RERO_DOC.NAVCOLLSPEC.VAUD
invenio collections create -q 'specific_collection.code:"SDC Deposit Library*"' -p RERO_DOC.NAVCOLLSPEC.VAUD RERO_DOC.NAVCOLLSPEC.VAUD.SDC_DEPOSIT_LIBRARY

# harvest articles and books on the production server
#invenio oaiharvester harvest --signals -u http://doc.rero.ch/oai2d -s "book" -d oia -m marcxml -k -e 'utf-8'
dojson -i data/book.xml -l marcxml do book schema http://rerodoc.test.rero.ch/schema/records/book-v0.0.1.json|invenio utils load -vv -m 100
