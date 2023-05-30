import pandas as pd
import os
import pyarrow.parquet as pq
from constants import DATA_DIR, ZONE_LOOKUP_FILENAME
from utils import get_data_filepath

zone_lookup = None

def load_zone_lookup():
    """Loads the zone lookup CSV file into a dictionary that maps location IDs to zones."""
    global zone_lookup
    filepath = os.path.join(DATA_DIR, ZONE_LOOKUP_FILENAME)
    zone_lookup = pd.read_csv(filepath, index_col='LocationID')['Zone'].to_dict()

def get_zone_by_id(location_id):
    """Returns the zone name for the given location ID."""
    global zone_lookup
    if zone_lookup is None:
        load_zone_lookup()
    return zone_lookup.get(location_id)

def load_data(year: int, month: int) -> pd.DataFrame:
    filepath = get_data_filepath(year, month, DATA_DIR)

    if not os.path.isfile(filepath):
        return None

    try:
        return pq.read_table(filepath).to_pandas()
    except Exception as e:
        print(f"Failed to load data from {filepath}. Error: {e}")
        return None


def load_data_for_year(year: int) -> pd.DataFrame:
    df_list = [load_data(year, month) for month in range(1, 13) if load_data(year, month) is not None]
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
