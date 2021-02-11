#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def add_current_load_runway(merged_df):
    '''
    Returns the dataframe passed as an input where
    a column representing the load on the runway was added.
    Here, the current load on the runway accounts for how many
    planes were taxiing at the same time and heading to the same
    runway when a specific aircraft starts taxiing.
    Input: Pandas dataframe object,
    Output: Pandas dataframe object with one extra column
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
        'runway', 'stand', 'AOBT', 'ATOT'
        ]]

    # performing the self-join on the variables flight_datetime_partial
    # and runway
    joined_df = merged_df_essential.merge(merged_df_essential, on=[
        'flight_datetime_partial', 'runway'], how='left',
        suffixes=(None, '_other'))

    # removing rows that contain the 2 same flights
    subset_joined_df = joined_df[
        joined_df['index'] != joined_df['index_other']
        ]

    # keeping only the rows where the aircraft is not taxiing at
    # the same time as another aicraft heading to the same runway
    subset_joined_df = subset_joined_df[(
        subset_joined_df['AOBT'] > subset_joined_df['AOBT_other'])
        & (subset_joined_df['AOBT'] < subset_joined_df['ATOT_other'])
        ]

    # counting the number of rows per different aircrafts
    # --> that accounts for counting the number of aircrafts taxiing
    # at the same time as a specific aircraft and heading to the same runway
    runway_load = subset_joined_df.groupby(['index'])['index_other']\
        .count().reset_index()

    # renaming the columns so that the names better reflect
    # the content of the columns
    runway_load.columns = ['index', 'current_load_on_runway']

    # adding the runway load to the merged_df
    # passed as an input to the function
    # we use the index to merge the two tables as they uniquely
    # identifies aircrafts/flights
    full_df = merged_df.merge(runway_load, on='index', how='left')

    # filling NaNs with 0 as that means that no corresponding
    # record was found, i.e. the load on the runway is null
    full_df.loc[
        full_df['current_load_on_runway'].isnull(), 'current_load_on_runway'
        ] = 0

    # removing extra columns that are not needed anymore
    full_df.drop(['flight_datetime_partial', 'index'], axis=1)

    return full_df
