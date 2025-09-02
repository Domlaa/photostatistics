import json
import subprocess
from pathlib import Path
from db import db_mysql
from db import db_sqlite
import hashlib

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

def log_raw_metadata(exiftool_path="exiftool"):
    folder = Path(r"C:\\Users\\ning\\Pictures\\Photo2025\\test")

    files = [str(f) for f in folder.rglob("*") if f.suffix.lower() in raw_ext_list]
    if not files:
        return

    print(f"find {len(files)} RAW file")

    # 分批执行，避免命令过长
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        print(f"reading {i}...")

        cmd = [exiftool_path, "-j"] + [f"-{tag}" for tag in TAGS] + batch
        print(f"cmd: {cmd}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        metadata_list = json.loads(result.stdout)

        for meta in metadata_list:
            # 按顺序拼接字段值
            concat_str = "|".join(str(meta.get(t, "")) for t in TAGS)
            # 生成 MD5
            md5_value = hashlib.md5(concat_str.encode("utf-8")).hexdigest()
            print(f"concat: {concat_str}, md5: {md5_value}, meta: {meta}")


def get_raw_metadata(folder_path, exiftool_path="exiftool"):
    folder = Path(folder_path)
    files = [str(f) for f in folder.rglob("*") if f.suffix.lower() in raw_ext_list]
    if not files:
        return []

    print(f"find {len(files)} RAW file")
    results = []
    # 分批执行，避免命令过长
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        print(f"reading {i}...")

        cmd = [exiftool_path, "-j"] + [f"-{tag}" for tag in TAGS] + batch
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        metadata_list = json.loads(result.stdout)

        for meta in metadata_list:
            # 按顺序拼接字段值
            concat_str = "|".join(str(meta.get(t, "")) for t in TAGS)
            # 生成 MD5
            md5_value = hashlib.md5(concat_str.encode("utf-8")).hexdigest()

            print(f"concat: {concat_str}, md5: {md5_value}")
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

    return results

def parse_focal_length(value: str) -> float:
    if isinstance(value, str):
        return float(value.replace("mm", "").strip())
    return float(value)


if __name__ == "__main__":
    # data = get_raw_metadata(r"E:\\Photo2024")
    # log_raw_metadata()

    data = get_raw_metadata(r"C:\\Users\\ning\\Pictures\\Photo2025\\1\\0112")
    # db_mysql.save_to_mysql(data, False)
    db_sqlite.save_to_sqlite(data, False)



