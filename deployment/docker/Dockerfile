FROM python:3.6.4-slim-stretch

LABEL maintainer="software@rero.ch"
LABEL description="RERO DOC Invenio application by RERO."

RUN apt-get update && apt-get install -y curl git gcc g++ cmake make\
    gnupg2 vim procps fontconfig libfontconfig1-dev\
    zlib1g zlib1g-dev libpng-dev lib32z1-dev\
    libjpeg-dev libtiff-dev libopenjp2-7-dev\
    && curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install -y nodejs \
    && pip install -U setuptools pip && \
    pip install -U virtualenv && \
    node --version && \
    npm install -g node-sass clean-css clean-css-cli requirejs uglify-js

WORKDIR /code

RUN echo "test"
# Poppler
RUN git clone git://git.freedesktop.org/git/poppler/poppler && \
    cd poppler; git checkout -b poppler-0.67.0

WORKDIR /code/poppler

RUN mkdir -p /code/poppler/build && cd /code/poppler/build \
    && cmake -Wno-dev -D ENABLE_XPDF_HEADERS=True ../ \
        && make -j 2 install

# make libpoppler globally available
RUN ldconfig /usr/local/lib

# Add Invenio sources to `code` and work there:
WORKDIR /rerodoc/rerodoc/src/rerodoc-app
COPY setup.py /rerodoc/rerodoc/src/rerodoc-app/
COPY setup.cfg /rerodoc/rerodoc/src/rerodoc-app/
COPY babel.ini /rerodoc/rerodoc/src/rerodoc-app/
COPY MANIFEST.in /rerodoc/rerodoc/src/rerodoc-app/
COPY README.rst /rerodoc/rerodoc/src/rerodoc-app/
COPY CHANGES.rst /rerodoc/rerodoc/src/rerodoc-app/
COPY requirements.txt /rerodoc/rerodoc/src/rerodoc-app/
COPY rerodoc_app /rerodoc/rerodoc/src/rerodoc-app/rerodoc_app
COPY data /rerodoc/data
COPY deployment/scripts/populate.sh /rerodoc/populate.sh
#COPY deployment/scripts/populate.sh /rerodoc/populate.sh
#COPY deployment/data/demo.json /rerodoc/data.json

# # Run container as user `invenio` with UID `1000`, which should match
# # current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' invenio && \
     chown -R invenio:invenio /rerodoc

USER invenio

SHELL ["/bin/bash", "-c"]
WORKDIR /rerodoc
RUN virtualenv rerodoc
RUN source rerodoc/bin/activate && \
    pip install cython && \
    pip install -r /rerodoc/rerodoc/src/rerodoc-app/requirements.txt && \
    pip install rerodoc/src/rerodoc-app && \
    pip install gunicorn

RUN source rerodoc/bin/activate && \
    invenio npm && \
    cd rerodoc/var/instance/static && \
    npm i && \
    invenio collect -v && \
    invenio assets build

USER root
RUN rm -rf /var/lib/apt/lists/*

USER invenio
CMD ["/rerodoc/rerodoc/bin/gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "invenio_app.wsgi"]
