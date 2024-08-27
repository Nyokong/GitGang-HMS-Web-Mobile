#!/bin/sh

export PGUSER="gitgang_postgres"

psql -c "CREATE DATABASE djangobackend"

# psql djangobackend -c "CREATE EXTENSION IF NOT EXISTS \"uuid=ossp\";"

