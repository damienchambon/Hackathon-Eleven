#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
pd.options.mode.chained_assignment = None


def join_datasets(df_airport, df_weather=None,
                  df_geography=None, df_aircraft=None):
    '''
    Returns a merged Pandas dataframe containing df_airport and all
    other dataframes that are provided as parameters.
    Input: Pandas dataframes objects,
    Output: Pandas dataframes object.
    '''

    merged_df = df_airport.copy()

    if df_weather is not None:
        # creating a new column for the hourly data
        # in the merged dataframe to join with the weather dataframe
        # we only keep the day and the hour
        merged_df['Flight_Datetime_modified'] = merged_df.apply(
            lambda x: x['Flight Datetime'][:-3], axis=1)

        # creating a transformed hourly data column
        # to join with the weather dataframe
        # we only keep the day and the hour
        df_weather_no_dup = df_weather.drop_duplicates()
        df_weather_no_dup['time_hourly_modified'] = df_weather_no_dup.apply(
            lambda x: x['time_hourly'][:-3], axis=1)

        # merging merged_df with df_weather
        merged_df = merged_df.merge(df_weather_no_dup,
                                    left_on='Flight_Datetime_modified',
                                    right_on='time_hourly_modified',
                                    how='left', suffixes=(None, '_copy'))

    if df_geography is not None:
        # getting the coordinates of the runway
        df_geography_runway = df_geography[
            ['runway', 'Lat_runway', 'Lng_runway']
            ]
        df_geography_runway_no_dup = df_geography_runway.drop_duplicates()

        # getting the coordinates of the stands
        df_geography_stand = df_geography[['stand', 'Lat_stand', 'Lng_stand']]
        df_geography_stand_no_dup = df_geography_stand.drop_duplicates()
        df_geography_stand_no_dup['stand'] = \
            df_geography_stand_no_dup['stand'].str.upper()

        # merging merged_df with df_geography
        merged_df = merged_df.merge(df_geography_runway_no_dup,
                                    left_on='Runway', right_on='runway',
                                    how='left', suffixes=(None, '_copy'))
        merged_df = merged_df.merge(df_geography_stand_no_dup,
                                    left_on='Stand', right_on='stand',
                                    how='left', suffixes=(None, '_copy'))

    if df_aircraft is not None:
        # creating a dictionary storing the correspondence
        # of the names of the models
        # the key is the name of the model (airport dataframe)
        # the value is the equivalent in aircraft characteristics dataframe
        pairs_rename_aircraft_models = {}
        pairs_rename_aircraft_models['A320-100/200'] = 'A320-200'
        pairs_rename_aircraft_models['A319'] = 'A319-100'
        pairs_rename_aircraft_models['B737-800 WINGLETS'] = \
            '737-800 with winglets'
        pairs_rename_aircraft_models['A321-100/200'] = 'A321-100'
        pairs_rename_aircraft_models['B777-200'] = '777-200'
        pairs_rename_aircraft_models['B787-900'] = '787-9 Dreamliner'
        pairs_rename_aircraft_models['ERJ-195'] = 'EMB 195 Standard'
        pairs_rename_aircraft_models['B757-200 WINGLETS'] = \
            '757-200, -200PF with winglets'
        pairs_rename_aircraft_models['B787-800 Dreamliner'] = \
            '787-8 Dreamliner'
        pairs_rename_aircraft_models['B747-400 Passenger'] = '747-400F'
        pairs_rename_aircraft_models['A320 NEO'] = 'A320neo Sharklet'
        pairs_rename_aircraft_models['A330-200'] = 'A330-200'
        pairs_rename_aircraft_models['A380-800'] = 'A380-800'
        pairs_rename_aircraft_models['A330-300'] = 'A330-300'
        pairs_rename_aircraft_models['ATR 72-500'] = 'ATR-42-500/"600"'
        pairs_rename_aircraft_models['B737-400'] = '737-400'
        pairs_rename_aircraft_models['ERJ-190'] = 'EMB 190 Standard'
        pairs_rename_aircraft_models['B737-700 WINGLETS'] = \
            '737-700 with winglets'
        pairs_rename_aircraft_models['A350-900'] = 'A350-900'
        pairs_rename_aircraft_models['DASH 8-Q400'] = 'Dash 8 Q400'
        pairs_rename_aircraft_models['B737-900ER'] = '737-900ER'

        # translating the names in merged_df
        merged_df['Aircraft_model_transformed'] = merged_df.apply(
            lambda x: pairs_rename_aircraft_models[x['Aircraft Model']]
            if x['Aircraft Model'] in pairs_rename_aircraft_models
            else '', axis=1)
        # removing rows where the equivalent model was not specified
        merged_df = merged_df[merged_df['Aircraft_model_transformed'] != '']

        # merging merged_df with df_aircraft
        merged_df = merged_df.merge(df_aircraft,
                                    left_on='Aircraft_model_transformed',
                                    right_on='A320-100',
                                    how='left', suffixes=(None, '_copy'))

    return merged_df
