from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyproj import Transformer, CRS
from datetime import datetime

def lon(x):
    # Define the source (EPSG:5973) and target (EPSG:4326) projections
    src_projection = CRS.from_string("EPSG:5973")
    dst_projection = CRS.from_string("EPSG:4326")

    # Use pyproj to perform the coordinate transformation
    transformer = Transformer.from_crs(src_projection, dst_projection)
    lon, lat = transformer.transform(x,0)

    # Print the converted coordinates in EPSG:4326
    return lon

def lat(x):
    # Define the source (EPSG:5973) and target (EPSG:4326) projections
    src_projection = CRS.from_string("EPSG:5973")
    dst_projection = CRS.from_string("EPSG:4326")

    # Use pyproj to perform the coordinate transformation
    transformer = Transformer.from_crs(src_projection, dst_projection)
    lon, lat = transformer.transform(0,x)

    # Print the converted coordinates in EPSG:4326
    return lat

# Pyspark session
spark = SparkSession.builder.appName("roadauthorityPreprocessCsv").master("local[*]").getOrCreate()

# Read the csv file, try to infer the schema
df = spark.read.option("header", True).csv("../raw-data/570_trafikkulykke-eksport.csv", inferSchema = True, sep=";")

df = df.withColumn("ULYKKESKLOKKESLETT", date_format(col("ULYKKESKLOKKESLETT"), "HH:mm:ss"))
df = df.withColumn("TIMESTAMP", concat_ws(' ', col("ULYKKESDATO"), col("ULYKKESKLOKKESLETT")).alias("TIMESTAMP"))

df = df.withColumn("COORDINATES", substring_index(substring_index(df["GEOMETRI"], "(", -1), ")", 1))
df = df.withColumn("LON", substring_index(df["COORDINATES"], " ", 1))
df = df.withColumn("COORDINATES", substring_index(df["COORDINATES"], " ", -2))
df = df.withColumn("LAT", substring_index(df["COORDINATES"], " ", 1))

start_date = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) #, tzinfo="Europe/Oslo") 

df = df.filter(col("TIMESTAMP") >= start_date)

# Select columns to keep
columns_to_keep = ['VEGSYSTEMREFERANSE', 'TIMESTAMP', 'FARTSGRENSE (KM/H)', 'VÆRFORHOLD', 'FØREFORHOLD', 'LYSFORHOLD', 'VEGBELYSNING (NY)', 'VEGBREDDE (M)', 'VEGTYPE', 'KJØREFELTTYPE', 'LON', 'LAT']
df = df.select(*columns_to_keep)

# Rename columns
name_mapping = {
    'VEGSYSTEMREFERANSE': 'RoadReference',
    'TIMESTAMP': 'Timestamp',
    'FARTSGRENSE (KM/H)': 'SpeedLimit(KMH)',
    'VÆRFORHOLD': 'Weather',
    'FØREFORHOLD': 'RoadConditions',
    'LYSFORHOLD': 'LightingConditions',
    'VEGBELYSNING (NY)': 'RoadLights',
    'VEGBREDDE (M)': 'RoadWidth(M)',
    'VEGTYPE': 'RoadType',
    'KJØREFELTTYPE': 'LaneType',
    'LON': 'Lon',
    'LAT': 'Lat'
}

# Use the select operation with alias to rename multiple columns
df = df.select([df[column].alias(new_name) for column, new_name in name_mapping.items()])



df.show(100, truncate=False)

#x = 262565.047
#y = 6649542.024

# Write dataframe to csv (Converted to pandas dataframe to avoid creating the csv as a folder)
#df.toPandas().to_csv("../datasets/accidents.csv", index=False)

# Stop context
spark.sparkContext.stop()