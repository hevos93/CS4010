# Importing libraries
import pandas as pd
from pyproj import Transformer, CRS

# Function to convert EPSG:5972 to EPSG:4326 in decimal degrees
def convert_gps(lon, lat):
    # Define the source (EPSG:5973) and target (EPSG:4326) projections
    src_projection = CRS.from_string("EPSG:5973")
    dst_projection = CRS.from_string("EPSG:4326")

    # Use pyproj to perform the coordinate transformation
    transformer = Transformer.from_crs(src_projection, dst_projection)
    converted_lon, converted_lat = transformer.transform(lon, lat)
    return converted_lon, converted_lat

# Reading the csv file
filename = '../datasets/accidents.csv'
df = pd.read_csv(filename)

# Create lists from dataframe lat, lon columns.
lon_list = df['Lon'].tolist()
lat_list = df['Lat'].tolist()

# Create empty lists for converted lat, lon
lon_list_converted = []
lat_list_converted = []

# Assuming lon_list and lat_list of equall length, loop through and convert every coordinate pair
counter = 0
while counter < len(lon_list):
    result = convert_gps(lon_list[counter], lat_list[counter])
    lon_list_converted.append(result[1]) 
    lat_list_converted.append(result[0]) 
    counter = counter + 1

# Turn the converted lists back into columns in the dataframe
df['Lon'] = pd.Series(lon_list_converted)
df['Lat'] = pd.Series(lat_list_converted)

# Save to csv
df.to_csv(filename, index=False, quoting=1)