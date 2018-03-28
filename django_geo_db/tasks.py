import os
import celery
app = celery.Celery('django_geo_db')

@app.task
def add(x, y):
    return x + y


app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
