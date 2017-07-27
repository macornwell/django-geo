#!/usr/bin/env bash
# This makes for debugging geo data and adding default data in quickly.
# It first drops precreated tables, then adds them all from the sql/ folder.
#
# Param 1: The directory to the sql table directory.
# Param 2: The database file.

sql_tables_directory=$1
database=$2

declare -a geotables=('django_geo_continent' 'django_geo_geocoordinate' 'django_geo_country' 'django_geo_zipcode' 'django_geo_state' 'django_geo_location' 'django_geo_city');
# Drop Geo Tables
for table in "${geotables[@]}"
do
	echo Dropping ${table};
	sqlite3 ${database} "drop table ${table}";
done

# Insert Geo Tables#!/usr/bin/env bash
for table in "${geotables[@]}"
do
    echo Inserting ${table};
    cat "${sql_tables_directory}/${table}.sql" | sqlite3 ${database}
done
