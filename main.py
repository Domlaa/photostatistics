import os

from common import utils
from process import process

os.makedirs('./data', exist_ok=True)

if __name__ == "__main__":
    _path = r"C:\Users\ning\Pictures\Photo2025\test"
    _file_name = "./data/0908.json"

    exif_data = process.get_exif_data(_path)
    print(f"exif_data {exif_data}")
    # data = get_raw_metadata(r"/Volumes/one/canon2025")
    # print(f"read file: {len(data)}")
    # 因为每次读取图片的exif信息，耗时较长，所以建议先读取存为json。
    # 再尝试存入 DB，这样即使失败或者想移植数据库，就无需重新读取。
    utils.save_json_file(exif_data, _file_name)





