# django-geo-db

A library that creates a geo empowered app in Django. This library contains both models and data for making geo in the US, straight forward.

## How to load default data 
The easiest way to import default data (although not the fastest) is by
using the django command 'setup_us_data'. This process can take quite awhile
as it will fill the database from continent down to zipcodes for all known US zipcodes.
This process will also create Location objects for each object as well.
