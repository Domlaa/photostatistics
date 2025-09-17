from dataclasses import dataclass
from typing import Optional


@dataclass
class ExifInfo:
    filename: str
    filepath: str
    model: Optional[str]
    lens: Optional[str]
    datetime: Optional[str]
    aperture: Optional[str]
    shutter: Optional[str]
    iso: Optional[int]
    focal_length: Optional[int]
    md5: str

