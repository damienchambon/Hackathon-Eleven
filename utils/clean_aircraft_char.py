#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


def clean_aircraft_char(dataset_path):
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
        'manufacturer', 'aircraft_model', 'engine class', 'number_engines',
        'approach_speed', 'wingtip_config', 'wingspan_feet', 'length_feet',
        'tail_height_feet', 'wheelbase_feet', 'cockpit_to_main_gear_feet',
        'main_gear_width', 'max_takeoff_weight', 'max_ramp_taxi_weight',
        'parking_area_square_feet', 'number_gear_types_tandem'
                             ]

    return subset_df_aircraft
