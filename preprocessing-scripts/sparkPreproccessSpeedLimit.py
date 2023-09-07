from pyspark.sql import SparkSession

# Pyspark session
spark = SparkSession.builder.appName("roadauthorityPreprocessCsv").master("local[*]").getOrCreate()

# Read the csv file, try to infer the schema
df = spark.read.option("header", True).csv("../raw-data/105_fartsgrense-eksport.csv", inferSchema = True, sep=";")

# Select columns to keep
columns_to_keep = ['VEGSYSTEMREFERANSE','STARTDATO', 'SLUTTDATO', 'FARTSGRENSE (KM/H)']
df = df.select(*columns_to_keep)

# Rename columns
name_mapping = {
    "VEGSYSTEMREFERANSE": "Vegreferanse",
    "STARTDATO": "Startdato",
    "SLUTTDATO": "Sluttdato",
    "FARTSGRENSE (KM/H)": "Fartsgrense"
}

# Use the select operation with alias to rename multiple columns
df = df.select([df[column].alias(new_name) for column, new_name in name_mapping.items()])

# Write dataframe to csv (Converted to pandas dataframe to avoid creating the csv as a folder)
df.toPandas().to_csv("../datasets/speed-limits.csv", index=False)

# Stop context
spark.sparkContext.stop()