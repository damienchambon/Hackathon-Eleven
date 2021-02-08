import pandas as pd
import numpy as np

def date2datetime_from_path(tsap_path,w_path,ac_path):

    ''' Different paths to select as inputs:
    - tsap_path: training_set_airport_data
    - w_path: weather_data
    - ac_path: aircraft_data '''

    ''' Importing Datasets '''
    training_set_airport_data = pd.read_csv('{}/training_set_airport_data.csv'
                                            .format(tsap_path))
    weather_data = pd.read_csv('{}/weather_data.csv'.format(w_path))
    xls = pd.ExcelFile('{}/ACchar.xlsx'.format(ac_path))
    aircraft_data = pd.read_excel(xls,'test')

    ''' Training Set Airport Data '''
    for idx_column in [0,2,3]:
        training_set_airport_data.iloc[:,idx_column] = pd.to_datetime(
                                training_set_airport_data.iloc[:,idx_column])

    ''' Weather Data '''
    weather_data.iloc[:,0] = pd.to_datetime(weather_data.iloc[:,0])

    ''' Aicraft Data '''
    aircraft_data.iloc[:,0] = pd.to_datetime(aircraft_data.iloc[:,0],
                                            errors = 'coerce')

    ''' Usage: df1,df2,df3 = date2datetime(p1,p2,p3)'''
    return training_set_airport_data, weather_data, aircraft_data


def date2datetime_from_pd(training_set_airport_data,weather_data,aircraft_data):

    ''' Different pandas to select as inputs:
    - training_set_airport_data
    - weather_data
    - aircraft_data '''

    ''' Training Set Airport Data '''
    for idx_column in [0,2,3]:
        training_set_airport_data.iloc[:,idx_column] = pd.to_datetime(
                                training_set_airport_data.iloc[:,idx_column])

    ''' Weather Data '''
    weather_data.iloc[:,0] = pd.to_datetime(weather_data.iloc[:,0])

    ''' Aicraft Data '''
    aircraft_data.iloc[:,0] = pd.to_datetime(aircraft_data.iloc[:,0],
                                            errors = 'coerce')

    ''' Usage: df1,df2,df3 = date2datetime(df1,df2,df3)'''
    return training_set_airport_data, weather_data, aircraft_data
