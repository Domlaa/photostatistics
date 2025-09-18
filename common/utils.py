import csv
import io
import json
import os
import platform

system = platform.system()


def parse_focal_length(value: str) -> float:
    if isinstance(value, str):
        return float(value.replace("mm", "").strip())
    return float(value)


def save_json_file(json_data, filename):
    # 保存为 JSON 文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def save_csv(output_str: str,
                  filename: str,
                  append_mode: bool):
    # 保存为 CSV 文件
    mode = "a" if append_mode else "w"
    with open(filename, mode, encoding="utf-8", newline="") as f:
        lines = output_str.splitlines()
        if append_mode:
            # 跳过表头
            lines = lines[1:]
        for line in lines:
            f.write(line + "\n")


def save_csv_file(output_str: str, filename: str, append_mode: bool):
    """保存 CSV 字符串到文件，自动处理表头和追加模式"""
    mode = "a" if append_mode else "w"
    file_exists = os.path.isfile(filename)

    # 把字符串当成文件解析
    reader = csv.reader(io.StringIO(output_str))
    rows = list(reader)

    if not rows:
        return  # 空数据就直接返回

    with open(filename, mode, encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)

        if append_mode:
            # 如果文件已存在，跳过表头
            if file_exists and len(rows) > 1:
                rows = rows[1:]

        writer.writerows(rows)



def is_macos() -> bool:
    return system == "Darwin"


def is_windows() -> bool:
    return system == "Windows"
