#!/usr/bin/env python3

from enum import Enum


class OnOffToggleEnum(str, Enum):
    on = "on"
    off = "off"
    toggle = "toggle"
