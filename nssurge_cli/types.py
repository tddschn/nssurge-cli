#!/usr/bin/env python3

from enum import Enum


class OnOffToggleEnum(str, Enum):
    on = "on"
    off = "off"
    toggle = "toggle"

class ChangeDeviceEnum(str, Enum):
    name = 'name' # type: ignore
    address = 'address'
    use_surge = 'shouldHandledBySurge'