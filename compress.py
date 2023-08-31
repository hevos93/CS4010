import zipfile
import os

zipped_folder_name = "container-data.zip"
folder_name = "container-data"
file_paths = []


print("Gathering files")
for root, directories, files in os.walk(folder_name):
    for filename in files:
        filepath = os.path.join(root, filename)
        file_paths.append(filepath)

print("Listing files to be compressed:")
for file_name in file_paths:
    print(file_name)

print("Starting Compression")
with zipfile.ZipFile(zipped_folder_name, "w") as zip:
    for file in file_paths:
        zip.write(file, compress_type=zipfile.ZIP_DEFLATED , compresslevel=9)

print("Completed compression")