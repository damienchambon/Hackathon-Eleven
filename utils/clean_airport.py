#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


def clean_airport(dataset_path):
    '''
    Returns a cleaned dataframe from a file containing
    the airport data
    file.
    Input: path of the CSV file,
    Output: Pandas dataframes object.
    '''

    df_airport = pd.read_csv(dataset_path)

    # removing flights where the block-out time is the
    # same as the take-off time
    df_airport = df_airport[~(df_airport['AOBT'] == df_airport['ATOT'])]

    return df_airport
