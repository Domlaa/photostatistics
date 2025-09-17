import hashlib
import json
import subprocess
from pathlib import Path

from common import utils
from common.timeit import timeit
from db.ExifInfo import ExifInfo

exiftool = "./exiftool/exiftool"

# 需要提取的 EXIF 字段
TAGS = [
    # "Make",                         # 相机品牌
    # "FileName",                     # 文件名
    "Model",  # 相机型号
    # "DateTimeOriginal",             # 拍摄日期
    "SubSecDateTimeOriginal",  # 拍摄日期 (使用毫秒，兼容连拍)
    "FNumber",  # 光圈
    "ExposureTime",  # 快门
    "ISO",  # ISO
    "LensModel",  # 镜头
    "FocalLength"  # 焦距
]

raw_ext_list = {".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng"}
batch_size = 100


@timeit
def get_raw_metadata(folder_path):
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
        batch = files[i:i + batch_size]
        print(f"reading {i}...")
        # -j 代表 json格式输出。
        # -后面接需要输出的标签
        # 最后接文件名，这里为数组
        cmd = [exiftool, "-j"] + [f"-{tag}" for tag in TAGS] + batch
        # print(f"cmd: {cmd}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        # print(f"result: {result.stdout}")
        metadata_list = json.loads(result.stdout)  # 固定数量的exif信息，列表
        # print(f"metadata_list: {metadata_list}")
        results.extend(metadata_list)

    return results


def handle_exif_info_array(metadata_list):
    results = []
    for meta in metadata_list:
        # 按顺序拼接字段值
        concat_str = "|".join(str(meta.get(t, "")) for t in TAGS)
        # 生成 MD5
        md5_value = hashlib.md5(concat_str.encode("utf-8")).hexdigest()
        # print(f"concat: {concat_str}, md5: {md5_value}")
        # print(f"meta: {meta}")
        focal_length_float = utils.parse_focal_length(meta.get("FocalLength"))
        results.append(parse_exif_map(meta, md5_value, focal_length_float))
    return results


def parse_exif_model(meta, md5_value, focal_length_float):
    return ExifInfo(
        model=meta.get("Model"),
        filename=Path(meta["SourceFile"]).name,
        datetime=meta.get("SubSecDateTimeOriginal"),
        aperture=meta.get("FNumber"),
        shutter=meta.get("ExposureTime"),
        iso=meta.get("ISO"),
        lens=meta.get("LensModel"),
        focal_length=int(focal_length_float),
        md5=md5_value,
        filepath=meta["SourceFile"],
    )


def parse_exif_map(meta, md5_value, focal_length_float) -> {}:
    return {
        "model": meta.get("Model"),
        "filename": Path(meta["SourceFile"]).name,
        "datetime": meta.get("SubSecDateTimeOriginal"),
        "aperture": meta.get("FNumber"),
        "shutter": meta.get("ExposureTime"),
        "iso": meta.get("ISO"),
        "lens": meta.get("LensModel"),
        "focal_length": int(focal_length_float),
        "md5": md5_value,
        "filepath": meta["SourceFile"],
    }


@timeit
def get_metadata(folder_path):
    results = []
    cmd = [exiftool, "-r", "-j", "-ext", "CR2"] + [f"-{tag}" for tag in TAGS] + [folder_path]
    print(f"cmd: {cmd}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    metadata_list = json.loads(result.stdout)
    utils.save_json_file(metadata_list, "./data/a.json")
    return results


def get_exif_data(_path):
    metadata_list = get_raw_metadata(_path)
    return handle_exif_info_array(metadata_list)
