#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import os
import site
from pathlib import Path
import importlib  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle5 as pickle

path = Path(os.getcwd())
site.addsitedir(path.parent)  

dataset_cleaning = importlib.import_module("Hackathon-Eleven.utils.dataset_cleaning")

# the datasets that are returned are cleaned
df_aircraft = dataset_cleaning.clean_aircraft(
    '/Users/valentinajerusalmi/Desktop/DSBA/YEAR_2/Hackaton/Resources/ACchar.xlsx'
    )

df_airport = dataset_cleaning.clean_airport(
    '/Users/valentinajerusalmi/Desktop/DSBA/YEAR_2/Hackaton/Resources/training_set_airport_data.csv'
    )

df_geography = dataset_cleaning.clean_geography(
    '/Users/valentinajerusalmi/Desktop/DSBA/YEAR_2/Hackaton/Resources/geographic_data.csv'
    )

df_weather = dataset_cleaning.clean_weather(
    '/Users/valentinajerusalmi/Desktop/DSBA/YEAR_2/Hackaton/Resources/Weather_data.csv'
    )

dataset_joining = importlib.import_module("Hackathon-Eleven.utils.dataset_joining")
merged_df = dataset_joining.join_datasets(df_airport, df_weather=df_weather,df_geography=df_geography, df_aircraft=df_aircraft)
pairs = pd.read_csv('/Users/valentinajerusalmi/Desktop/DSBA/YEAR_2/Hackaton/LocalFolder/new_pairs.csv')
pairs.columns = ['index','stand','runway','distance']
with open('./df_apt_time.pkl', "rb") as fh:
    N_Q_df = pickle.load(fh)
    

X, y = Preprocessing(merged_df, pairs, N_Q_df)