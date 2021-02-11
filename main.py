#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main(root_dir, train_mode, test_mode, path_model):

    # importing packages used here
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    import os
    import site
    from pathlib import Path
    import importlib  
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import lightgbm as lgb
    import pickle
    
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import GridSearchCV

    # importing our packages
    dataset_cleaning = importlib.import_module(
        "Hackathon-Eleven.utils.dataset_cleaning"
        )
    dataset_joining = importlib.import_module(
        "Hackathon-Eleven.utils.dataset_joining"
        )
    add_current_load_runway = importlib.import_module(
        "Hackathon-Eleven.utils.add_current_load_runway"
        )
    add_current_load_airport_N_Q = importlib.import_module(
        "Hackathon-Eleven.utils.add_current_load_airport_N_Q"
        )
    add_shortest_path_length = importlib.import_module(
        "Hackathon-Eleven.utils.add_shortest_path_length"
        )
    preprocessing = importlib.import_module(
        "Hackathon-Eleven.utils.preprocessing"
        )
    train = importlib.import_module(
        "Hackathon-Eleven.utils.train"
        )

    if train_mode == True:
        # the datasets that are returned are cleaned
        df_aircraft = dataset_cleaning.clean_aircraft(
            root_dir+'/Resources/ACchar.xlsx'
            )
    
        df_airport = dataset_cleaning.clean_airport(
            root_dir+'/Resources/training_set_airport_data.csv',
            mode='train'
            )
    
        df_geography = dataset_cleaning.clean_geography(
            root_dir+'/Resources/geographic_data.csv'
            )
    
        df_weather = dataset_cleaning.clean_weather(
            root_dir+'/Resources/Weather_data.csv',
            mode='train'
            )
    
        merged_df = dataset_joining.join_datasets(
            df_airport, df_weather=df_weather,
            df_geography=df_geography, df_aircraft=df_aircraft
            )

        pairs = pd.read_csv(root_dir+'/Resources/new_pairs.csv')
        pairs.columns = ['index', 'stand', 'runway', 'distance']

        X, y = preprocessing.preprocessing(merged_df, pairs)

        fitted_model = train.train(X, y)

        # storing the model in the specified path
        filehandler = open(path_model, 'w')
        pickle.dump(fitted_model, filehandler)
    
    if test_mode == True:
        
        # loading the model
        filehandler = open(path_model, 'r')
        fitted_model = pickle.load(filehandler)
        
        # the datasets that are returned are cleaned
        df_aircraft = dataset_cleaning.clean_aircraft(
            root_dir+'/Resources/ACchar.xlsx'
            )

        df_airport = dataset_cleaning.clean_airport(
            root_dir+'/Resources/test_set_airport_data.xlsx',
            mode='test'
            )

        df_geography = dataset_cleaning.clean_geography(
            root_dir+'/Resources/geographic_data.csv'
            )

        df_weather = dataset_cleaning.clean_weather(
            root_dir+'/Resources/test_set_weather_data.xlsx',
            mode='test'
            )

        merged_df = dataset_joining.join_datasets(
            df_airport, df_weather=df_weather,
            df_geography=df_geography, df_aircraft=df_aircraft
            )

        pairs = pd.read_csv(root_dir+'/Resources/new_pairs.csv')
        pairs.columns = ['index', 'stand', 'runway', 'distance']

        X, y = preprocessing.preprocessing(merged_df, pairs)

        
main('/Users/damienchambon/Desktop/ETUDES/M2 2020-2021/Hackathon',train_mode=True,test_mode=False)




