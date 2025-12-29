"""
Quick and dirty remplacement for pb_tool

edit: for some reasons dezip and rezip the output to make it works

"""

import configparser

config = configparser.ConfigParser()

config.read('../pb_tool.cfg')


plugin_name_dir = config["plugin"]["name"]

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

    output_path = "../"

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(f"{plugin_name_dir}.zip", mode="w")
    try:
        for file_name in file_names:
            zf.write(output_path + file_name, file_name, compress_type=compression)

    except FileNotFoundError as e:
        print("An error occurred:", e)
    finally:
        # Don't forget to close the file!
        zf.close()



compress(file_names)
