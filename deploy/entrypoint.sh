echo "Waiting for postgres..."

# Abort on any error (including if wait-for-it fails).
set -e

/market/deploy/wait-for-it.sh postgres:$DB_PORT

echo "PostgreSQL started"
#cd ./market
#alembic upgrade head
#alembic revision --autogenerate -m "New Migration"

exec "$@"
