import os
import urllib.request
import zipfile
import argparse
import pandas as pd
import pyarrow.parquet as pq
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

pd.options.mode.chained_assignment = None

DATA_DIR = 'data'
PLOT_DIR = 'plots'
SHAPEFILE_FILENAME = 'taxi_zones.zip'
SHAPEFILE_URL = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip'
ZONE_LOOKUP_FILENAME = 'taxi+_zone_lookup.csv'
ZONE_LOOKUP_URL = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv'

zone_lookup = None

def download_and_extract_shapefile():
    shapefile_filepath = os.path.join(DATA_DIR, SHAPEFILE_FILENAME)
    if os.path.exists(shapefile_filepath):
        print(f'Shapefile already exists. Skipping download.')
        return

    print(f'Downloading and extracting shapefile...')
    urllib.request.urlretrieve(SHAPEFILE_URL, shapefile_filepath)

    with zipfile.ZipFile(shapefile_filepath, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)

    print(f'Shapefile downloaded and extracted successfully.')

def download_zone_lookup():
    """Downloads the zone lookup CSV file and saves it in the data directory."""
    url = ZONE_LOOKUP_URL
    filename = ZONE_LOOKUP_FILENAME
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(filepath):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"File {filename} downloaded successfully.")

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

def get_data_url(year: int, month: int) -> str:
    return f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"

def get_data_filepath(year: int, month: int, folder: str) -> str:
    filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
    return os.path.join(folder, filename)


def create_dir_if_not_exists(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)


def check_and_download_file(url: str, filepath: str):
    filename = url.split("/")[-1]

    if os.path.isfile(filepath):
        print(f"File {filename} already exists. Skipping download.")
        return

    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"File {filename} downloaded successfully.")
    except Exception as e:
        print(f"Failed to download file {filename}. Error: {e}")


def download_data(year: int, month: int):
    create_dir_if_not_exists(DATA_DIR)
    url = get_data_url(year, month)
    filepath = get_data_filepath(year, month, DATA_DIR)
    check_and_download_file(url, filepath)


def download_all_files_for_year(year: int):
    for month in range(1, 13):
        download_data(year, month)


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


def preprocess_data(df: pd.DataFrame, year: int, month: int):
    start_date = pd.Timestamp(f'{year}-{month:02d}-01')
    end_date = start_date + pd.DateOffset(months=1)
    mask = (df['tpep_pickup_datetime'] >= start_date) & (df['tpep_pickup_datetime'] < end_date)
    df = df.loc[mask]

    df['pickup_day'] = df['tpep_pickup_datetime'].dt.to_period('D')
    df['route'] = df['PULocationID'].apply(get_zone_by_id) + '-' + df['DOLocationID'].apply(get_zone_by_id)
    return df


def most_frequent_routes(num_of_routes: int, year: int, month: int):
    df = load_data(year, month)
    if df is None:
        return
    
    filename = f'frequent-routes-{year}-{month:02d}.png'
    print(f'Generating {filename}...')

    df = preprocess_data(df, year, month)

    top_routes = df['route'].value_counts().nlargest(num_of_routes).index.tolist()
    df_top_routes = df[df['route'].isin(top_routes)]

    df_grouped = df_top_routes.groupby(['pickup_day', 'route']).size().reset_index(name='count')
    df_pivot = df_grouped.pivot(index='pickup_day', columns='route', values='count')

    plt.figure(figsize=(10, 6))
    for column in df_pivot.columns:
        plt.plot(df_pivot.index.strftime('%d'), df_pivot[column], label=column)
    plt.xlabel('Day of the Month')
    plt.ylabel('Number of Rides')
    plt.title(f'{num_of_routes} Most Frequent Routes {year}-{month:02d}')
    plt.legend()
    plt.xticks(range(0, 31))

    create_dir_if_not_exists(PLOT_DIR)
    filepath = os.path.join(PLOT_DIR, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)

def plot_departures_per_zone(year: int, month: int):
    df = load_data(year, month)
    if df is None:
        return

    filename = f'departures-per-zone-{year}-{month:02d}.png'
    print(f'Generating {filename}...')

    # Preprocess data and count departures per zone
    departures_per_zone = preprocess_data(df, year, month)['PULocationID'].value_counts()

    # Load taxi zones shapefile and merge departures count with taxi zones
    taxi_zones = gpd.read_file('data/taxi_zones.shp').set_index('LocationID')
    taxi_zones['departures'] = departures_per_zone

    fig, ax = plt.subplots()
    taxi_zones.plot(column='departures', ax=ax, cmap='viridis', linewidth=0.8, edgecolor='0.8',
                    norm=colors.LogNorm(vmin=departures_per_zone.min(), vmax=departures_per_zone.max()), 
                    legend=True, legend_kwds={'label': "Number of Departures", 
                                              'orientation': "vertical"})

    # Format and set colorbar labels
    colorbar = ax.get_figure().get_axes()[1]
    colorbar.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

    # Remove bottom and left axis labels and set title
    ax.set_axis_off()
    plt.title(f'Taxi Departures per Zone {year}-{month:02d}')

    # Save figure
    create_dir_if_not_exists(PLOT_DIR)
    plt.savefig(os.path.join(PLOT_DIR, filename), bbox_inches='tight', dpi=300)


def main():
    parser = argparse.ArgumentParser(description='Process taxi trip data.')
    parser.add_argument('--year', type=int, help='The year of the data to process.')
    parser.add_argument('--month', type=int, help='The month of the data to process.')

    args = parser.parse_args()

    year = args.year if args.year else 2023
    month = args.month if args.month else 1
    download_zone_lookup()
    download_and_extract_shapefile()

    if args.month or (args.month is None and args.year is None):
        download_data(year, month)
        most_frequent_routes(3, year, month)
        plot_departures_per_zone(year, month)
    else:
        download_all_files_for_year(year)
        for month in range(1, 13):
            most_frequent_routes(3, year, month)
            plot_departures_per_zone(year, month)

if __name__ == '__main__':
    main()
