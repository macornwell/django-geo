import io
from django.conf import settings
from celery import shared_task
from celery.result import AsyncResult
from django_geo_db.models import CeleryPlottedMapTask, CELERY_STATUS_CHOICES, PlottedMap, \
    CELERY_SUCCESS, CELERY_STARTED, LocationMapType, LocationMap, LocationBounds, Location
from django_geo_db.utilities import plot_map
from django_geo_db.storage import DataStorage
from django_geo_db.utilities import LatLon


def check_on_map_status(plotted_map):
    task = CeleryPlottedMapTask.objects.get(plotted_map=plotted_map)
    result = AsyncResult(task.task_id)
    status = ''
    results_status = result.status
    for small, large in CELERY_STATUS_CHOICES:
        larger = large.upper()
        # Find the equivical status
        if result.status == larger:
            # See if we need to perform an update.
            if task.status != small:
                # update
                pass
            status = large
    return status


@shared_task(bind=True)
def start_plot_map(self, plotted_map_id, coordinate_strings, domain, location_map_id,
                   map_bounds_id, marker, marker_size_percent, task_id=None):
    """
    Plots coordinates
    :param plotted_map:
    :param coordinates:
    :param storage:
    :param base_location_map:
    :param map_bounds:
    :param marker:
    :param marker_size_percent:
    :param task_id:
    :return:
    """
    coordinates = [LatLon.parse_string(s) for s in coordinate_strings]

    plotted_map = PlottedMap.objects.get(pk=plotted_map_id)
    location_map = LocationMap.objects.get(pk=location_map_id)
    bounds = LocationBounds.objects.get(pk=map_bounds_id)

    storage = DataStorage(domain)
    map_task = CeleryPlottedMapTask()
    map_task.status = CELERY_STARTED
    map_task.task_id = start_plot_map.request.id
    map_task.plotted_map = plotted_map
    map_task.save()

    combined = plot_map(coordinates, storage, location_map, bounds, marker, marker_size_percent)

    directory = 'plotted_maps'
    filename = str(self.request.id) + '.png'
    combined = io.BytesIO(combined)
    plotted_map.map_file_url = settings.MEDIA_URL + storage.save_file_get_url(combined, directory, filename)
    plotted_map.save()
    map_task.status = CELERY_SUCCESS
    map_task.save()
    return
