import pandas as pd
def load_data(file):
    df = pd.read_csv(file, parse_dates=True, index_col=0)
    df.index = pd.to_datetime(df.index)
    return df

#sorting data
def preprocess_data(df,date_col, target_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]) #converted the date column to datetime
    df = df[[date_col, target_col]] #only using 2 columns and dropping the other columns
    df = df.sort_values(by=date_col)
    df = df.dropna()
    return df

