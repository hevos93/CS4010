# Importing libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Pyspark session
spark = SparkSession.builder.appName("roadauthorityPreprocessCsv").master("local[*]").getOrCreate()

# Read the csv file, try to infer the schema
df = spark.read.option("header", True).csv("../raw-data/105_fartsgrense-eksport.csv", inferSchema = True, sep=";")

# Filtering on active speed limits
df = df.filter(df.SLUTTDATO.isNull())

# Splitting out speed limit meter locations
df = df.filter(~ df.VEGSYSTEMREFERANSE.like("%KD%"))
df = df.filter(~ df.VEGSYSTEMREFERANSE.like("%SD%"))
df = df.withColumn("LENGDE", split(df.VEGSYSTEMREFERANSE, 'RV162 S1D1 m')[1])
df = df.withColumn("LENGDE", split(df.LENGDE, '-'))
df = df.withColumn("METER_TIL", df.LENGDE[1])
df = df.withColumn("METER_FRA", df.LENGDE[0])

# Select and rename columns
name_mapping = {
    "VEGSYSTEMREFERANSE": "Vegreferanse",
    "FARTSGRENSE (KM/H)": "Fartsgrense",
    "METER_FRA": "Meter_Fra",
    "METER_TIL": "Meter_Til"
}

# Use the select operation with alias to rename multiple columns
df = df.select([df[column].alias(new_name) for column, new_name in name_mapping.items()])

# Write dataframe to csv (Converted to pandas dataframe to avoid creating the csv as a folder)
df.toPandas().to_csv("../datasets/speed-limits.csv", index=False)

# Stop context
spark.sparkContext.stop()