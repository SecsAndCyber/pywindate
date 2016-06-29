from datetime import datetime

WINDOWS_TICK = 10000000
SEC_TO_UNIX_EPOCH = 11644473600

def FileTimeToDateTime( file_time_64 ):
    unix_time = ((file_time_64 / WINDOWS_TICK) - SEC_TO_UNIX_EPOCH) & 0xFFFFFFFF
    return datetime.utcfromtimestamp(unix_time)
    
def DateTimeToFileTime( date_time ):
    unix_time = int((date_time - datetime(1970,1,1)).total_seconds())
    return ((unix_time + SEC_TO_UNIX_EPOCH) * WINDOWS_TICK) & 0xFFFFFFFFFFFFFFFF