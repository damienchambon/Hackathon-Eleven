import os
import pandas as pd
import numpy as np

def date2datetime(path):

    ''' Changing OS Directory to Data Path (Input) '''
    os.chdir(path)

    ''' Importing Datasets '''
    training_set_airport_data = pd.read_csv('training_set_airport_data.csv')
    weather_data = pd.read_csv('weather_data.csv')
    xls = pd.ExcelFile('ACchar.xlsx')
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

    ''' Usage: df1,df2,df3 = date2datetime(data_path)'''
    return training_set_airport_data, weather_data, aircraft_data
