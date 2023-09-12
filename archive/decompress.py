import zipfile

zipped_folder_name = "container-data.zip"

print("Decompressing" + zipped_folder_name)
with zipfile.ZipFile(zipped_folder_name, "r") as zipped_folder:
    zipped_folder.extractall()

print("Completed decompressing")