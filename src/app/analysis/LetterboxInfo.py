"""
Module: LetterboxInfo.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Data class containing info about applied letter-boxing that was done onto the image to make it
    into desired resolution without changing ratio ratio
"""

from dataclasses import dataclass


@dataclass
class LetterboxInfo:
    scale: float
    paddingLeft: int
    paddingTop: int
