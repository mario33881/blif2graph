#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imports modules and packages for the user that executes:
python -m blif2graph
"""

from ._version import __version__  # noqa: F401

try:
    from . import blif2graph

except ImportError:
    from .blif2graph import blif2graph

if __name__ == "__main__":
    blif2graph.main()