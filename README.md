# NYC yellow taxi trip data visualization

Data is taken from: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Currently Implemented visualizations:
- Most frequent routes by day (pyplot)
- Number of departures per zone per month (geoplot)

## Usage examples
- Generate plots for all months of 2022:
    
    ```
    python3 main.py --year 2022
    ```

- Generate plots for month 03 of year 2023:

    ```
    python3 main.py --year 2023 --month 3
    ```

Note: making graphs for data of the whole year needs to be improved as it uses too much memory.