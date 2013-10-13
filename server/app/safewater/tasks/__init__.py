
from celery.task import task

from twitter import Twitter
from swdis import Swdis

@task
def monitor_twitter():
    mine = Twitter()
    return mine.monitor()

@task
def import_violations():
    mine = Swdis()
    return mine.import_violations()

@task
def import_pws():
    mine = Swdis()
    return mine.import_pws()
