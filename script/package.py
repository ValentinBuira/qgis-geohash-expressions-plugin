"""
Quick and dirty remplacement for pb_tool

"""

import configparser
import os


base_path = os.path.dirname(__file__)

config_file_path = os.path.join(base_path, '../pb_tool.cfg')
plugin_path = os.path.join(base_path, "../")
zip_build_path = os.path.join(base_path, "../zip_build/")
metadata_path = os.path.join(base_path, "../metadata.txt")


if not os.path.exists(zip_build_path):
    os.makedirs(zip_build_path)

config = configparser.ConfigParser()
config.read(config_file_path)

metadata = configparser.ConfigParser()
metadata.read(metadata_path)

plugin_name_dir = config["plugin"]["name"]
plugin_version = metadata["general"]["version"]

file_names = []
for cat in config["files"]:
    print(cat)
    l = config["files"][cat].split(" ")
    file_names.extend(l)
    print(l)

file_names = [f for f in file_names if f != '']


import zlib
import zipfile

def compress(file_names):
    print("File Paths:")
    print(file_names)

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(os.path.join(zip_build_path, f"{plugin_name_dir}_v{plugin_version}.zip"), mode="w")
    try:
        for file_name in file_names:
            zf.write(plugin_path + file_name,
                     arcname=plugin_name_dir +"/" + file_name,
                     compress_type=compression)

    except FileNotFoundError as e:
        print("An error occurred:", e)
    finally:
        # Don't forget to close the file!
        zf.close()



compress(file_names)
