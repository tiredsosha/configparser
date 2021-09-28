import re
import yaml

from typing import Optional, Union
from ipaddress import IPv4Address
from pydantic import BaseModel, validator


class App(BaseModel):
    en_zone: str
    ru_zone: Optional[str] = None
    ip: Optional[IPv4Address] = None
    mac: Optional[str] = None
    five_themes: Optional[bool] = True
    lasers: Optional[int] = None
    composers: Optional[int] = None
    body: Optional[int] = None
    depth: Optional[int] = None
    game_en_name: Optional[str] = None
    game_ru_name: Optional[str] = None
    file_name: Optional[str] = None
    scenes: Optional[dict] = None
    led: Optional[bool] = False


with open('configparser/configs/apps.yaml') as yam:
    fruits_list = yaml.safe_load(yam)


def from_dict(data):
    d = {}
    for k, v in data.items():
        d[k] = App(**v)
    return d


print(from_dict(fruits_list))