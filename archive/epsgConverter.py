from pyproj import Transformer, CRS

# Define the source (EPSG:5973) and target (EPSG:4326) projections
src_projection = CRS.from_string("EPSG:5973")
dst_projection = CRS.from_string("EPSG:4326")

# Coordinates in EPSG:5973 (X, Y)
x = 262565.047
y = 6649542.024

# Use pyproj to perform the coordinate transformation
transformer = Transformer.from_crs(src_projection, dst_projection)
lon, lat = transformer.transform(x, y)

# Print the converted coordinates in EPSG:4326
print(f"Longitude (EPSG:4326): {lon}")
print(f"Latitude (EPSG:4326): {lat}")