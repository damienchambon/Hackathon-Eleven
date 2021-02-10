#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
pd.options.mode.chained_assignment = None
import datetime

def clean_weather_data(dataset_path):
    '''
    Returns a cleaned dataframe from a file containing
    the weather data
    file.
    Input: path of the CSV file,
    Output: Pandas dataframes object.
    '''

    df_weather = pd.read_csv(dataset_path)

    # dropping duplicates as there are several weather records per hour
    df_weather = df_weather.drop_duplicates()

    # changing the time_hourly variable to a datetime format
    df_weather.iloc[:, 0] = pd.to_datetime(
        df_weather.iloc[:, 0], errors='coerce'
        )
    df_weather = df_weather[
        df_weather['time_hourly'].dt.date <= datetime.date(2018, 12, 31)
        ]

    # reducing the number of different values of the variable summary
    # focusing on dangerously windy
    df_weather.loc[
        df_weather['summary'] == 'Dangerously Windy and Partly Cloudy',
        'summary'] = 'Dangerously Windy'
    df_weather.loc[
        df_weather['summary'] == 'Dangerously Windy and Overcast',
        'summary'] = 'Dangerously Windy'
    df_weather.loc[
        df_weather['summary'] == 'Possible Light Rain and Dangerously Windy',
        'summary'] = 'Dangerously Windy'
    df_weather.loc[
        df_weather['summary'] == 'Dangerously Windy and Mostly Cloudy',
        'summary'] = 'Dangerously Windy'
    df_weather.loc[
        df_weather['summary'] == 'Possible Drizzle and Dangerously Windy',
        'summary'] = 'Dangerously Windy'
    df_weather.loc[
        df_weather['summary'] == 'Light Rain and Dangerously Windy',
        'summary'] = 'Dangerously Windy'
    df_weather.loc[
        df_weather['summary'] == 'Flurries',
        'summary'] = 'Dangerously Windy'

    # focusing on cloudy
    df_weather.loc[
        df_weather['summary'] == 'Mostly Cloudy',
        'summary'] = 'Cloudy'
    df_weather.loc[
        df_weather['summary'] == 'Overcast',
        'summary'] = 'Cloudy'
    df_weather.loc[
        df_weather['summary'] == 'Partly Cloudy',
        'summary'] = 'Cloudy'

    # focusing on rain and wind
    df_weather.loc[
        df_weather['summary'] == 'Light Rain and Windy',
        'summary'] = 'Rain and Wind'
    df_weather.loc[
        df_weather['summary'] == 'Possible Drizzle and Windy',
        'summary'] = 'Rain and Wind'
    df_weather.loc[
        df_weather['summary'] == 'Possible Light Rain and Windy',
        'summary'] = 'Rain and Wind'

    # focusing on clouds and wind
    df_weather.loc[
        df_weather['summary'] == 'Windy and Partly Cloudy',
        'summary'] = 'Clouds and Wind'
    df_weather.loc[
        df_weather['summary'] == 'Windy and Mostly Cloudy',
        'summary'] = 'Clouds and Wind'
    df_weather.loc[
        df_weather['summary'] == 'Windy and Overcast',
        'summary'] = 'Clouds and Wind'
    df_weather.loc[
        df_weather['summary'] == 'Windy',
        'summary'] = 'Clouds and Wind'

    # focusing on light rain
    df_weather.loc[
        df_weather['summary'] == 'Light Rain',
        'summary'] = 'Rain'

    # removing variables that have very low variance or a lot of missing values
    # also removing the apparentTemperature variable because it is highly
    # correlated with the other temperature variable
    df_weather = df_weather.drop([
        'precipAccumulation', 'precipType', 'precipIntensity',
        'precipProbability', 'pressure', 'icon', 'ozone', 'apparentTemperature'
         ], axis=1)

    # filling missing values with last valid value
    # we do that because we deal with weather data and the weather
    # at a specific hour is ikely to be similar to the
    # last recorded information
    df_weather = df_weather.fillna(method='ffill')

    return df_weather
