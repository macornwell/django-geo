import csv
from django.core.management.base import BaseCommand
from django_geo_db.models import Country, State, County, StateRegion

class Command(BaseCommand):
    help = "Imports a csv containing state region information."

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str)

    def __handle_row(self, country, state, county, region):
        pass

    def handle(self, *args, **options):
        countries = {}
        country_to_state = {}
        country_to_state_to_region = {}
        with open(options['csv_file_path']) as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                country = row[0].lower()
                state = row[1].lower()
                region = row[2]
                county = row[3].lower()
                try:
                    if country not in countries:
                        country_obj = Country.objects.get(name__iexact=country)
                        countries[country] = country_obj
                        country_to_state[country] = {}
                        country_to_state_to_region[country] = {}
                    country_obj = countries[country]
                    if state not in country_to_state[country]:
                        state_obj = State.objects.get(country=country_obj, name__iexact=state)
                        country_to_state[country][state] = state_obj
                        country_to_state_to_region[country][state] = {}
                    state_obj = country_to_state[country][state]
                    if region not in country_to_state_to_region[country][state]:
                        try:
                            region_obj = StateRegion.objects.get(state=state_obj, name=region)
                        except:
                            region_obj = StateRegion(state=state_obj, name=region)
                            print('Creating Region {0}'.format(region_obj))
                            region_obj.save()
                        country_to_state_to_region[country][state][region] = region_obj
                    region_obj = country_to_state_to_region[country][state][region]
                    county_obj = County.objects.get(state=state_obj, name__iexact=county)

                    if region_obj not in county_obj.stateregion_set.all():
                        print('Adding {0} into region {1}'.format(county_obj, region_obj))
                        region_obj.counties.add(county_obj)
                        region_obj.save()
                    else:

                        print('Already found {0} in region {1}. Skipping.'.format(county_obj, region_obj))
                except:
                    print(row)
                    raise



