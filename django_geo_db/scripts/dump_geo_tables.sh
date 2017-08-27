#!/bin/bash
# A script that creates populated .sql files for quick ingesting.
# This should ONLY be used if the models have been changed.
#
# Param 1: The directory to the sql table directory.
# Param 2: The database file.

sql_tables_directory=$1
database=$2

declare -a geotables=('django_geo_db_continent' 'django_geo_db_geocoordinate' 'django_geo_db_country' 'django_geo_db_zipcode' 'django_geo_db_state' 'django_geo_db_location' 'django_geo_db_city');
for table in "${geotables[@]}"
do
    echo Dumping ${table};
    sqlite3 ${database} ".dump ${table}" > ${sql_tables_directory}/${table}.sql
done
