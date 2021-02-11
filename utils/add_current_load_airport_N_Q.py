#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def add_current_load_airport_N_Q(merged_df):
    '''
    Function that computes the N number of aircrafts moving 
    when the airplane starts taxing and also Q, which are 
    the number of aircrafts that finished the movement while 
    the aircraft in focus is still moving.
    Input: Pandas dataframe object,
    Output: Pandas dataframe object with 2 extra columns
    '''

    # taking only the partial datetime, as we will use it self join
    # the dataframe --> that helps speed up the self join
    merged_df['flight_datetime_partial'] = merged_df\
        .apply(lambda x: x['flight_datetime'].date(), axis=1)

    # creating an index so we can identify flights
    merged_df['index'] = merged_df.index

    # taking a subset of the columns so that the self-join is faster
    merged_df_essential = merged_df[[
        'index', 'flight_datetime', 'flight_datetime_partial',
        'AOBT', 'ATOT'
        ]]

    # performing the self-join on the variable flight_datetime_partial
    joined_df = merged_df_essential.merge(merged_df_essential, on=[
        'flight_datetime_partial'], how='left',
        suffixes=(None, '_other'))

    # removing rows that contain the 2 same flights
    subset_joined_df = joined_df[
        joined_df['index'] != joined_df['index_other']
        ]

    # keeping only the rows where other aircrafts are already
    # taxiing on the airport surface at the time that the
    # particular aircraft starts to taxi
    df_N = subset_joined_df[(
        subset_joined_df['AOBT'] > subset_joined_df['AOBT_other'])
        & (subset_joined_df['AOBT'] < subset_joined_df['ATOT_other'])
        ]

    # keeping only the rows where other aircrafts cease taxiing
    # during the time that the particular aircraft is taxiing
    df_Q = df_N[(df_N['ATOT'] > df_N['ATOT_other'])]

    # counting the number of rows per different aircrafts
    # --> that accounts for counting the number of aircrafts already
    # taxiing on the airport surface at the time that the particular aircraft
    # starts to taxi
    df_N_load = df_N.groupby(['index'])['index_other']\
        .count().reset_index()

    # renaming the columns so that the names better reflect
    # the content of the columns
    df_N_load.columns = ['index', 'load_N']

    # adding the load to the merged_df
    # passed as an input to the function
    # we use the index to merge the two tables as they uniquely
    # identifies aircrafts/flights
    full_df = merged_df.merge(df_N_load, on='index', how='left')

    # filling NaNs with 0 as that means that no corresponding
    # record was found, i.e. the load on the runway is null
    full_df.loc[
        full_df['load_N'].isnull(), 'load_N'
        ] = 0

    # counting the number of rows per different aircrafts
    # --> that accounts for counting the number of aircrafts taxiing
    # during the time that the particular aircraft is taxiing
    df_Q_load = df_Q.groupby(['index'])['index_other']\
        .count().reset_index()

    # renaming the columns so that the names better reflect
    # the content of the columns
    df_Q_load.columns = ['index', 'load_Q']

    # adding the load to the merged_df
    # passed as an input to the function
    # we use the index to merge the two tables as they uniquely
    # identifies aircrafts/flights
    full_df = full_df.merge(df_Q_load, on='index', how='left')

    # filling NaNs with 0 as that means that no corresponding
    # record was found, i.e. the load on the runway is null
    full_df.loc[
        full_df['load_Q'].isnull(), 'load_Q'
        ] = 0

    # removing extra columns that are not needed anymore
    full_df.drop(['flight_datetime_partial', 'index'], axis=1)

    return full_df
