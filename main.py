import os

from common import utils
from process import process

os.makedirs('./data', exist_ok=True)

if __name__ == "__main__":
    _path = r"C:\Users\ning\Pictures\Photo2025\test"
    _file_name = "./data/test.json"

    data = process.get_raw_metadata(_path)
    # data = get_raw_metadata(r"/Volumes/one/canon2025")
    print(f"read file: {len(data)}")
    # 因为每次读取图片的exif信息，耗时较长，所以建议先读取存为json。
    # 再尝试存入 DB。
    utils.save_json_file(data, _file_name)




