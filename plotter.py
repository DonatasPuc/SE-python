import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import geopandas as gpd
from utils import create_dir_if_not_exists
from constants import PLOT_DIR
from data_loader import load_data
from data_preprocessor import preprocess_data

def plot_most_frequent_routes(num_of_routes: int, year: int, month: int):
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
