# Author: Donatas Pučinskas
import argparse
from data_downloader import download_zone_lookup, download_and_extract_shapefile, download_data, download_all_files_for_year
from plotter import plot_most_frequent_routes, plot_departures_per_zone

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
        plot_most_frequent_routes(3, year, month)
        plot_departures_per_zone(year, month)
    else:
        download_all_files_for_year(year)
        for month in range(1, 13):
            plot_most_frequent_routes(3, year, month)
            plot_departures_per_zone(year, month)

if __name__ == '__main__':
    main()
