import json


def parse_focal_length(value: str) -> float:
    if isinstance(value, str):
        return float(value.replace("mm", "").strip())
    return float(value)


def save_json_file(json_data, filename):
    # 保存为 JSON 文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
