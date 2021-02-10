import pandas as pd
import numpy as np

def preprocess_training_from_path(path):
    df = pd.read_csv('{}/training_set_airport_data.csv'.format(path))

    if df.iloc[:,0].dtypes != "dtype('<M8[ns]')":
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
    if df.iloc[:,2].dtypes != "dtype('<M8[ns]')":
        df.iloc[:,2] = pd.to_datetime(df.iloc[:,2])
    if df.iloc[:,3].dtypes != "dtype('<M8[ns]')":
        df.iloc[:,3] = pd.to_datetime(df.iloc[:,3])


    df['taxi_out'] = df.iloc[:,3] - df.iloc[:,2]
    df['taxi_out']= df.taxi_out.dt.seconds/60

    df['delay_block_out'] = abs(df.iloc[:,2] - df.iloc[:,0])
    df['delay_block_out'] = df.delay_block_out.dt.seconds/60

    return df

def preprocess_training_from_pandas(df):

    if df.iloc[:,0].dtypes != "dtype('<M8[ns]')":
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
    if df.iloc[:,2].dtypes != "dtype('<M8[ns]')":
        df.iloc[:,2] = pd.to_datetime(df.iloc[:,2])
    if df.iloc[:,3].dtypes != "dtype('<M8[ns]')":
        df.iloc[:,3] = pd.to_datetime(df.iloc[:,3])


    df['taxi_out'] = df.iloc[:,3] - df.iloc[:,2]
    df['taxi_out']= df.taxi_out.dt.seconds/60

    df['delay_block_out'] = abs(df.iloc[:,2] - df.iloc[:,0])
    df['delay_block_out'] = df.delay_block_out.dt.seconds/60

    return df
