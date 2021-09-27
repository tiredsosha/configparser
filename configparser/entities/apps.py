from typing import Optional
import pydantic
import yaml

class Main(pydantic.BaseModel):
    enname: str
    runame: str


with open('configparser/test.yaml') as yam:
    fruits_list = yaml.safe_load(yam)

def from_dict(data):
    d = {}
    for k, v in data.items():
        d[k] = Main(**v)
    return d

ma = from_dict(fruits_list)
print(ma)