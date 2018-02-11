import csv
import collections

MAIN_PATH = 'django_geo_db/data/us-cities-and-zips.csv'
COUNTY_PATH = 'django_geo_db/data/us_zip_codes_states.csv'
OUT_FILE = 'django_geo_db/data/us-data-final.csv'


def combine():
    all_entries = {}
    all_entries_by_state_name = {}
    print('Reading first file')
    with open(MAIN_PATH, 'r') as inFile:
        reader = csv.reader(inFile)
        is_first = True
        #zip,city,state,latitude,longitude,timezone,dst
        for line in reader:
            if is_first:
                is_first = False
                continue
            entry = [
                line[0],
                line[1],
                line[2],
                line[3],
                line[4],
                line[5],
                line[6],
            ]
            state = entry[2]
            city = entry[1]
            if state not in all_entries_by_state_name:
                all_entries_by_state_name[state] = {}
            if city not in all_entries_by_state_name[state]:
                all_entries_by_state_name[state][city] = entry
            zip = int(entry[0])
            all_entries[zip] = entry
    print('Reading second file')
    with open(COUNTY_PATH, 'r') as inFile:
        reader = csv.reader(inFile)
        is_first = True
        #zip_code,latitude,longitude,city,state,county
        for line in reader:
            if is_first:
                is_first = False
                continue
            zipcode = int(line[0])
            county = line[5]
            state = line[4]
            city = line[3]
            lat = line[1]
            if not lat:
                continue
            if city == 'Apo' or city == 'Fpo':
                continue
            if zipcode == '40129':
                continue
            if city == 'Migrate' and state == 'KY':
                continue
            if city == 'Mc Lean':
                city = 'McLean'
            if state == 'GU' or state == 'PW' or state == 'FM' or state == 'MP' or state == 'MH':
                continue
            if zipcode not in all_entries:
                if city == 'East Boston':
                    city = 'Boston'
                if city == 'North Waltham':
                    city = 'Waltham'
                try:
                    another_version = all_entries_by_state_name[state][city]
                except Exception as e:
                    print(state)
                    print(city)
                    raise e
                lat = another_version[3]
                lon = another_version[4]
                time = another_version[5]
                dst = another_version[6]
                print('{0} - {1}, {2} was not found. Adding.'.format(zipcode, city, state))
                all_entries[zipcode] = [
                    zipcode, city, state, lat, lon, time, dst
                ]
            all_entries[zipcode].insert(3, county)
    print('Writing Results')
    # Reorder them
    all_entries_in_order = collections.OrderedDict()
    all_zips = sorted([int(key) for key in all_entries.keys()])
    for zip in all_zips:
        all_entries_in_order[zip] = all_entries[zip]

    with open(OUT_FILE, 'w') as outFile:
        writer = csv.writer(outFile)
        writer.writerow(['zip', 'city', 'state', 'county', 'latitude', 'longitude', 'timezone', 'dst'])
        for zip, entry in all_entries_in_order.items():
            if len(entry) != 8:
                continue
            writer.writerow(entry)
    print('Done')
combine()
