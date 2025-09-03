import json
import os
import subprocess
from pathlib import Path
from db import db_mysql
from db import db_sqlite
import hashlib
import platform

# 需要提取的 EXIF 字段
TAGS = [
    #"Make",                         # 相机品牌
    # "FileName",                     # 文件名
    "Model",                        # 相机型号
    #"DateTimeOriginal",             # 拍摄日期
    "SubSecDateTimeOriginal",       # 拍摄日期 (使用毫秒，兼容连拍)
    "FNumber",                      # 光圈
    "ExposureTime",                 # 快门
    "ISO",                          # ISO
    "LensModel",                    # 镜头
    "FocalLength"                   # 焦距
]

raw_ext_list = {".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng"}
batch_size=100

def get_raw_metadata(folder_path, exiftool_path="exiftool"):
    folder = Path(folder_path)
    files = [
        str(f)
        for f in folder.rglob("*")
        if f.suffix.lower() in raw_ext_list and not f.name.startswith("._")
    ]
    if not files:
        return []

    print(f"find {len(files)} RAW file")
    results = []

    # 分批执行，避免命令过长
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        print(f"reading {i}...")

        cmd = [exiftool_path, "-j"] + [f"-{tag}" for tag in TAGS] + batch
        # print(f"cmd: {cmd}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        metadata_list = json.loads(result.stdout)
        results.extend(metadata_list)

    return results

def handle_exif_info_array(metadata_list):
    results = []
    for meta in metadata_list:
        # 按顺序拼接字段值
        concat_str = "|".join(str(meta.get(t, "")) for t in TAGS)
        # 生成 MD5
        md5_value = hashlib.md5(concat_str.encode("utf-8")).hexdigest()
        print(f"concat: {concat_str}, md5: {md5_value}")
        # print(f"meta: {meta}")
        results.append({
            # "make": meta.get("Make"),
            "model": meta.get("Model"),
            "filename": Path(meta["SourceFile"]).name,
            "datetime": meta.get("SubSecDateTimeOriginal"),
            "aperture": meta.get("FNumber"),
            "shutter": meta.get("ExposureTime"),
            "iso": meta.get("ISO"),
            "lens": meta.get("LensModel"),
            "focal_length": parse_focal_length(meta.get("FocalLength")),
            "md5": md5_value,
            "filepath": meta["SourceFile"],
        })
    # db_mysql.save_to_mysql(data, False)
    # db_sqlite.save_to_sqlite(data, True)

def parse_focal_length(value: str) -> float:
    if isinstance(value, str):
        return float(value.replace("mm", "").strip())
    return float(value)


def save_json_file(json_data, filename):
    # 保存为 JSON 文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    data = get_raw_metadata(r"E:\\Photo2024")
    # data = get_raw_metadata(r"/Volumes/one/canon2025")
    print(f"read file: {len(data)}")
    save_json_file(data, "canon2024.json")




