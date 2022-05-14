#!/usr/bin/env python3


from enum import Enum

class OnOffEnum(str, Enum):
    on = "on"
    off = "off"