import os
import urllib.request
import zipfile
from utils import create_dir_if_not_exists, get_data_url, get_data_filepath
from constants import DATA_DIR, SHAPEFILE_FILENAME, SHAPEFILE_URL, ZONE_LOOKUP_FILENAME, ZONE_LOOKUP_URL

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