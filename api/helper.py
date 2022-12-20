import logging
from django_db_logger.models import StatusLog


def SaveLog(e):
    print(e)
    db_logger = logging.getLogger('accounts')
    db_logger.exception(e)

def checkTrueOrFalse(str):
    if str == 1 or str == "1" or str == "TRUE" or str == "true" or str == "True":
        return True
    
    if str == 0 or str == "0" or str == "FALSE" or str == "false" or str == "False":
        return False

def ValueCheck(value):
    try:
        if value is None:
            return ""
        else:
            return str(value)
    except Exception as e:
        SaveLog(e)
        return ""