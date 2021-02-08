import datetime
import calendar
import numpy as np


def week_day(date_time):
    '''
    Returns an integer value corresponding to the day of the week.
    Input: datetime object,
    Output: integer.
    '''
    return date_time.isoweekday()


def get_weekday(date_time):
    '''
    Returns the day of the week for a given datetime object.
    Input: datetime object,
    Output: string (upper).
    '''
    output = calendar.day_name[date_time.weekday()].upper()
    return output


def get_month(date_time):
    ''' Returns an integer value correponding to the given month.
    Input: datetime object,
    Output: integer.
    '''
    return date_time.month


def get_year(date_time):
    '''
    Returns the year of a given datetime.
    Input: datetime object,
    Output: integer.
    '''
    return date_time.year


def get_day(date_time):
    '''
    Returns the day (integer) of a given datetime.
    Input: datetime object,
    Output: integer.
    '''
    return date_time.day


def create_datetime(y,m,d):
    '''
    Inputs: {y = year, m = month, d = day}
    Output: datetime object with selected values.
    '''
    return datetime.datetime(year = y, month = m, day = d)


def int2datetime(myintdate):
    '''
    Input: AAAAMMDD as integer,
    Output: datetime object with selected values.
    '''
    aaaa = int(np.floor(myintdate/10000))
    mm = int(np.floor(myintdate/100) - aaaa*100)
    dd = int(myintdate - aaaa*10000 - mm*100)
    return create_datetime(aaaa,mm,dd)


def str2datetime(AAAAMMDD):
    '''
    Input: AAAAMMDD as string,
    Output: datetime object with selected values.
    '''
    return  datetime.datetime.strptime(AAAAMMDD, "%Y%m%d")


def datetime2str(date_time):
    '''
    Input: datetime object,
    Output: AAAA-MM-DD as string.
    '''
    return  str(date_time)[:10]


def datetime2singlestr(date_time):
    '''
    Input: datetime object,
    Output: 'AAAAMMDD' as single string.
    '''
    return str(date_time)[:4] + str(date_time)[5:7] + str(date_time)[8:10]


def str2timestamp(string):
    ''' Converts a string to a timestamp format. '''
    return (datetime.datetime(year = int(string[0:4]), month = int(string[4:6]),
                            day = int(string[6:8]), hour = int(string[8:10]),
                            minute = int(string[10:12]) ) )


def date_slash(date_time):
    '''
    Input: datetime object,
    Output: DD/MM/AAAA HH:minute:second,microsecond.
    '''

    return str(date_time.day) + "/" + str(date_time.month) + "/" +
                str(date_time.year) + " " + str(date_time.hour) + ":" +
                str(date_time.minute) + ":" +str(date_time.second) + "," +
                str(date_time.microsecond)


def date_nodash(date_time):
    ''' Removes dashes from datetime, returns a single string.'''
    return(str(date_time).replace('-',''))
