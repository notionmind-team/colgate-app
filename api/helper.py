import logging
from django_db_logger.models import StatusLog


def SaveLog(e):
    print(e)
    db_logger = logging.getLogger('accounts')
    db_logger.exception(e)
