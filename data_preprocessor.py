import pandas as pd
from data_loader import get_zone_by_id

def preprocess_data(df: pd.DataFrame, year: int, month: int):
    start_date = pd.Timestamp(f'{year}-{month:02d}-01')
    end_date = start_date + pd.DateOffset(months=1)
    mask = (df['tpep_pickup_datetime'] >= start_date) & (df['tpep_pickup_datetime'] < end_date)
    df = df.loc[mask]

    df = df.copy()
    df['pickup_day'] = df['tpep_pickup_datetime'].dt.to_period('D')
    df['route'] = df['PULocationID'].apply(get_zone_by_id) + '-' + df['DOLocationID'].apply(get_zone_by_id)
    return df
