#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main(root_dir, train_mode, test_mode):

    # importing packages used here
    from sklearn.model_selection import train_test_split
    import os
    import site
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
        "utils.dataset_cleaning"
        )
    dataset_joining = importlib.import_module(
        "utils.dataset_joining"
        )
    preprocessing = importlib.import_module(
        "utils.preprocessing"
        )
    train = importlib.import_module(
        "utils.train"
        )

    if train_mode == True:
        # the datasets that are returned are cleaned
        print('Cleaning the datasets...')
        df_aircraft = dataset_cleaning.clean_aircraft(
            root_dir+'/resources/ACchar.xlsx'
            )
    
        df_airport = dataset_cleaning.clean_airport(
            root_dir+'/resources/training_set_airport_data.csv',
            mode='train'
            )
    
        df_geography = dataset_cleaning.clean_geography(
            root_dir+'/resources/geographic_data.csv'
            )
    
        df_weather = dataset_cleaning.clean_weather(
            root_dir+'/resources/Weather_data.csv',
            mode='train'
            )

        print('Merging the datasets...')
        merged_df = dataset_joining.join_datasets(
            df_airport, df_weather=df_weather,
            df_geography=df_geography, df_aircraft=df_aircraft
            )

        pairs = pd.read_csv(root_dir+'/resources/new_pairs.csv')
        pairs.columns = ['index', 'stand', 'runway', 'distance']

        print('Preprocessing the data...')
        X, y = preprocessing.preprocessing(merged_df, pairs, 'train', root_dir)

        print('Fitting the model...')
        fitted_model = train.train(X, y)

        print('Saving the model...')
        # storing the model in the specified path
        filehandler = open(root_dir+'/models/model.pkl', 'w')
        pickle.dump(fitted_model, filehandler)
    
    if test_mode == True:
        
        # loading the model
        filehandler = open(path_model, 'r')
        fitted_model = pickle.load(filehandler)

        # the datasets that are returned are cleaned
        df_aircraft = dataset_cleaning.clean_aircraft(
            root_dir+'/resources/ACchar.xlsx'
            )

        df_airport = dataset_cleaning.clean_airport(
            root_dir+'/resources/test_set_airport_data.xlsx',
            mode='test'
            )

        df_geography = dataset_cleaning.clean_geography(
            root_dir+'/resources/geographic_data.csv'
            )

        df_weather = dataset_cleaning.clean_weather(
            root_dir+'/resources/test_set_weather_data.xlsx',
            mode='test'
            )

        merged_df = dataset_joining.join_datasets(
            df_airport, df_weather=df_weather,
            df_geography=df_geography, df_aircraft=df_aircraft
            )

        pairs = pd.read_csv(root_dir+'/resources/new_pairs.csv')
        pairs.columns = ['index', 'stand', 'runway', 'distance']

        X, y = preprocessing.preprocessing(merged_df, pairs, 'test', root_dir)
 
main('/Users/damienchambon/Desktop/ETUDES/M2 2020-2021/Hackathon/Hackathon-Eleven',train_mode=True,test_mode=False)




