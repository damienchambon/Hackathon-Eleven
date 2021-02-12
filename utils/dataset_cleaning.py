#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
pd.options.mode.chained_assignment = None


def clean_airport(dataset_path, mode):
    '''
    Returns a cleaned dataframe from a file containing
    the airport data
    file.
    Input: path of the CSV file,
    Output: Pandas dataframes object.
    '''
    if mode == 'train':
        df_airport = pd.read_csv(dataset_path)
    else:
        df_airport = pd.read_excel(dataset_path)

    # removing flights where the block-out time is the
    # same as the take-off time
    df_airport = df_airport[~(df_airport['AOBT'] == df_airport['ATOT'])]

    # changing the name of the columns so they are better formatted
    df_airport.columns = [
        'flight_datetime', 'aircraft_model', 'AOBT',
        'ATOT', 'stand', 'runway'
        ]

    # changing the flight_datetime variable to a datetime format
    df_airport.iloc[:, 0] = pd.to_datetime(
        df_airport.iloc[:, 0], errors='coerce'
        )

    return df_airport


def clean_geography(dataset_path):
    '''
    Returns a cleaned dataframe from a file containing
    the weather data
    file.
    Input: path of the CSV file,
    Output: Pandas dataframes object.
    '''

    df_geography = pd.read_csv(dataset_path)

    # removing duplicate rows
    df_geography = df_geography.drop_duplicates()

    return df_geography


def clean_aircraft(dataset_path):
    '''
    Returns a cleaned dataframe from a file containing
    the aircraft characteristics, where the file is an Excel file
    file.
    Input: path of the Excel file,
    Output: Pandas dataframes object.
    '''
    # we assume the file is an Excel file, where the
    # aircraft characteristics are on the second sheet
    df_aircraft = pd.read_excel(dataset_path, sheet_name=1)

    # selecting only the aircrafts we keep for the study
    # they account for 99% of the flights we study
    list_aircrafts_to_keep = [
        'A320-200', 'A319-100', '737-800 with winglets', 'A321-100', '777-200',
        '787-9 Dreamliner', 'EMB 195 Standard',
        '757-200, -200PF with winglets', '787-8 Dreamliner', '747-400F',
        'A320neo Sharklet', 'A330-200', 'A380-800', 'A330-300',
        'ATR-42-500/"600"', '737-400', 'EMB 190 Standard',
        '737-700 with winglets', 'A350-900', 'Dash 8 Q400', '737-900ER'
        ]
    subset_df_aircraft = df_aircraft[df_aircraft['A320-100']
                                     .isin(list_aircrafts_to_keep)]

    # dropping some columns
    # columns that are not useful for the model (strings, identifiers)
    list_col_to_remove = [
        'Date Completed', 'ICAO Code', 'Years Manufactured', 'Note'
        ]
    # columns of categories linked to actual values already
    # present in the dataframe
    list_col_to_remove += [
        'AAC', 'ADG', 'TDG', 'ATCT Weight Class', 'Wake Category'
        ]
    subset_df_aircraft = subset_df_aircraft \
        .drop(list_col_to_remove, axis='columns')

    # manually inputing the missing values after doing online research
    # adding # engines
    subset_df_aircraft.loc[
        subset_df_aircraft['A320-100'] == 'Dash 8 Q400', '# Engines'
        ] = 2
    # setting correct MGW
    subset_df_aircraft.loc[
        subset_df_aircraft['A320-100'] == 'ATR-42-500/"600"',
        'MGW\n(Outer to Outer)'
        ] = 16
    # setting correct Main Gear Config
    subset_df_aircraft.loc[
        subset_df_aircraft['A320-100'] == 'A380-800', 'Main Gear Config'
        ] = '2D'
    subset_df_aircraft.loc[
        subset_df_aircraft['A320-100'] == '747-400F', 'Main Gear Config'
        ] = '2D'

    # modifying the main gear config variable format
    # changing values like 'D' to '1D'
    subset_df_aircraft['Main Gear Config'] = subset_df_aircraft \
        .apply(lambda x: '1'+x['Main Gear Config']
               if len(x['Main Gear Config']) == 1
               else x['Main Gear Config'], axis=1)
    # creating a new variable to only include part of the main gear config
    subset_df_aircraft['number_gear_types_tandem'] = subset_df_aircraft \
        .apply(lambda x: x['Main Gear Config'][0], axis=1)
    # dropping the main gear config variable altogether
    subset_df_aircraft = subset_df_aircraft.drop(
        ['Main Gear Config'], axis='columns')

    # replacing some manufacturer values
    subset_df_aircraft.loc[
        (subset_df_aircraft['Manufacturer'] != 'Boeing') &
        (subset_df_aircraft['Manufacturer'] != 'Airbus'),
        'Manufacturer'] = 'Other'

    # renaming the name of the columns
    subset_df_aircraft.columns = [
        'manufacturer', 'full_aircraft_model', 'engine class', 'number_engines',
        'approach_speed', 'wingtip_config', 'wingspan_feet', 'length_feet',
        'tail_height_feet', 'wheelbase_feet', 'cockpit_to_main_gear_feet',
        'main_gear_width', 'max_takeoff_weight', 'max_ramp_taxi_weight',
        'parking_area_square_feet', 'number_gear_types_tandem'
                             ]

    return subset_df_aircraft


def clean_weather(dataset_path,mode):
    '''
    Returns a cleaned dataframe from a file containing
    the weather data
    file.
    Input: path of the CSV file,
    Output: Pandas dataframes object.
    '''
    if mode == 'train':
        df_weather = pd.read_csv(dataset_path)
    else:
        df_weather = pd.read_excel(dataset_path)

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
