import yaml

from typing import Optional
from ipaddress import IPv4Address
from pydantic import validator, BaseModel


class Park(BaseModel):
    admin_ip: IPv4Address
    language: str = True
    username: Optional[str] = "ShrWAPek"
    password: Optional[str] = "O403seL"
    theme: str = True

    @validator("language")
    def lang_to_bool(cls, val):
        val = val.lower()
        if "en" in val:
            value = True
        elif "ru" in val:
            value = False
        else:
            raise ValueError(
                f"\nПоле Language принимает только значения en/ru\nИсправь park.yaml"
            )
        return value

    @validator("theme")
    def theme_to_bool(cls, val):
        val = val.lower()
        if "hp" in val:
            value = True
        elif "hc" in val:
            value = False
        else:
            raise ValueError(
                f"\nПоле Theme принимает только значения hc/hp. Исправь park.yaml"
            )
        return value

    @validator("username", always=True)
    def set_username(cls, val):
        return val or "ShrWAPek"

    @validator("password", always=True)
    def set_password(cls, val):
        return val or "O403seL"
