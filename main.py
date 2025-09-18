import os

from common import utils
from process import process

os.makedirs('./data', exist_ok=True)

if __name__ == "__main__":
    _path = r"C:\Users\ning\Pictures\Photo2025\test"
    if utils.is_macos():
        _path = r"/Volumes/one/canon2025/0501"
    _file_name = "./data/a.json"

    process.save_metadata_by_csv(_path, "./data/b.csv")
    # exif_data = process.get_exif_data(_path)
    # print(f"exif_data {exif_data}")
    # utils.save_json_file(exif_data, _file_name)
