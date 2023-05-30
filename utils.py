import os

def create_dir_if_not_exists(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_data_url(year: int, month: int) -> str:
    return f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"

def get_data_filepath(year: int, month: int, folder: str) -> str:
    filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
    return os.path.join(folder, filename)