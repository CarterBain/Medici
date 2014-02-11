#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.ExecutionFilter -> config module for ExecutionFilter.java.

"""
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.lib.overloading import overloaded',
    ]
