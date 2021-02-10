#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


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
