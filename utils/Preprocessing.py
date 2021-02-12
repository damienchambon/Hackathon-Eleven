import pandas as pd


def preprocessing(merged_df, pairs, mode):

    # Merge with the distances between stands and runways
    merged_df = pd.merge(merged_df, pairs,  how='left',
                         left_on=['stand', 'runway'],
                         right_on=['stand', 'runway'])

    if mode = 'train':
        # Adding target variable
        merged_df.iloc[:, 2] = pd.to_datetime(
            merged_df.iloc[:, 2], errors='coerce')
        merged_df.iloc[:, 3] = pd.to_datetime(
            merged_df.iloc[:, 3], errors='coerce')
        variable = abs(merged_df.iloc[:, 3] - merged_df.iloc[:, 2])
        merged_df['taxi_out'] = variable.astype('int64')/(6*10**10)
        
        # Remove outliers
        merged_df = merged_df[merged_df['taxi_out'] < 500]
    else:
        merged_df.iloc[:, 2] = pd.to_datetime(
            merged_df.iloc[:, 2], errors='coerce')

    # Drop null records
    merged_df = merged_df.dropna()


    # Adding the N and Q variables
    #merged_df = merged_df.merge(N_Q_df[['Flight Datetime', 'ATOT', 'N', 'Q' ]], 
      #                          left_on=['flight_datetime', 'ATOT'], right_on=['Flight Datetime', 'ATOT' ], 
     #                           suffixes=(False, False))
    merged_df = add_current_load_airport_N_Q.add_current_load_airport_N_Q(merged_df)
    
    # Adding an interaction variable between N and Q
    merged_df['interaction_N_Q'] = merged_df['load_N']*merged_df['load_Q']

    # Adding current load of the runway as a variable
    merged_df = add_current_load_runway.add_current_load_runway(merged_df)
    
    # Adding the length of the shortest path between stand and runway
    # for each flight
    merged_df = add_shortest_path_length.add_shortest_path_length(merged_df)

    # Adding the delay variable between Block Out Time and Flight Date Time
    merged_df['delay'] = (-1)**(merged_df['AOBT'] <
                                merged_df['flight_datetime']) * \
        abs(merged_df['flight_datetime'] - merged_df['AOBT']).dt.seconds/60

    # Isolating the target variable y
    y = merged_df.pop('taxi_out')

    # Training set X
    X = merged_df

    # Adding the day of the week
    X['flight_day'] = X['flight_datetime'].dt.day_name()

    # Adding the name of the month
    X['flight_month'] = X['flight_datetime'].dt.month_name()

    # Adding the specific moments of the day
    val = (X['flight_datetime'].dt.hour % 24 + 4) // 4
    val.replace({1: 'Late Night',
                 2: 'Early Morning',
                 3: 'Morning',
                 4: 'Noon',
                 5: 'Evening',
                 6: 'Night'}, inplace=True)

    X['day_moment'] = val

    # Drop of the useless variables
    X = X.drop(['Flight Datetime', 'Lat_runway', 'Lng_runway',
                'Lat_stand', 'Lng_stand', 'flight_datetime',
                'aircraft_model', 'AOBT', 'ATOT', 'stand', 'index',
                'time_hourly', 'manufacturer', 'full_aircraft_model'], axis=1)

    # Transformation of categorical variables into numerical
    # features when necessary
    X['number_engines'] = pd.to_numeric(X['number_engines'], downcast="float")
    X['wingspan_feet'] = pd.to_numeric(X['wingspan_feet'], downcast="float")
    X['length_feet'] = pd.to_numeric(X['length_feet'], downcast="float")
    X['tail_height_feet'] = pd.to_numeric(X['tail_height_feet'],
                                          downcast="float")
    X['wheelbase_feet'] = pd.to_numeric(X['wheelbase_feet'], downcast="float")
    X['cockpit_to_main_gear_feet'] = pd.to_numeric(
        X['cockpit_to_main_gear_feet'],
        downcast="float")
    X['main_gear_width'] = pd.to_numeric(
        X['main_gear_width'],
        downcast="float")
    X['max_takeoff_weight'] = pd.to_numeric(
        X['max_takeoff_weight'],
        downcast="float")
    X['max_ramp_taxi_weight'] = pd.to_numeric(
        X['max_ramp_taxi_weight'],
        downcast="float")
    X['parking_area_square_feet'] = pd.to_numeric(
        X['parking_area_square_feet'],
        downcast="float")


    #ONE HOT ENCODING

    # Selecting categorical features
    cat_column_names = X.select_dtypes('object').columns.tolist()

    # Fit of the encoder on the training set
    ohe = OneHotEncoder(
        sparse=False,
        handle_unknown='ignore'
    )
    
    # converting categories into strings (so that Null values would be treated as a category per se)
    ohe.fit(X[cat_column_names].astype(str))

    # from numpy to dataframe
    new_column_names = [
        f"{category} - {level}" for category, level_list in zip(cat_column_names, ohe.categories_)
        for level in level_list]

    X_ohe = pd.DataFrame(
        ohe.transform(X[cat_column_names].astype(str)),
        index=X.index,
        columns=new_column_names)

    # Drop of the old categorical features 
    X = pd.concat([
        X.drop(cat_column_names, axis=1),
        X_ohe], axis=1)

    # SCALING THE FEATURES
    scaler = StandardScaler()
    num_cols = ['temperature', 'dewPoint', 'humidity', 'windSpeed',
                'windGust', 'windBearing', 'cloudCover', 'uvIndex',
                'visibility', 'approach_speed', 'distance', 'load_N',
                'load_Q', 'interaction_N_Q', 'current_load_on_runway',
                'shortest_path_length']
    X[num_cols] = scaler.fit_transform(X[num_cols])

    return X, y
