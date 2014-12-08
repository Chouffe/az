#!/bin/bash

LOGS_DIRECTORY="logs"
DB_DIRECTORY="/data/db"

if [ ! -d "$LOGS_DIRECTORY" ]; then
  mkdir $LOGS_DIRECTORY
fi

if [ ! -d "$DB_DIRECTORY" ]; then
  mkdir $DB_DIRECTORY
fi

echo "Starting the db"
mongod > "$LOGS_DIRECTORY/db.log" 2>&1 &
sleep 2
echo "Starting the services"
echo "Starting the main server"
python services/server.py > "$LOGS_DIRECTORY/server.log" 2>&1 &
echo "Starting the ml service"
python services/ml_service.py > "$LOGS_DIRECTORY/ml.log" 2>&1 &
echo "Starting the demo service"
python services/demo_service.py > "$LOGS_DIRECTORY/demo.log" 2>&1 &
cd webapp
echo "Starting the webapp"
lein run
# > "$LOGS_DIRECTORY/webapp.log" 2>&1 &
cd -
