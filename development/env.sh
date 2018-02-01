
export FLASK_DEBUG=0
export INVENIO_SEARCH_ELASTIC_HOSTS=localhost
export INVENIO_SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://rerodoc:rerodoc@localhost:5432/rerodoc
export INVENIO_CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
export INVENIO_CELERY_RESULT_BACKEND=redis://localhost:6379/1
export INVENIO_CACHE_REDIS_URL='redis://localhost:6379/1'
export INVENIO_ACCOUNTS_SESSION_REDIS_URL='redis://localhost:6379/0'
export INVENIO_DB_VERSIONING=0
export INVENIO_APP_ENABLE_SECURE_HEADERS=0
