#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Part of XLSX to Odoo import
# Copyright 2019 David Todd <dtodd@oceantech.com>
# License: MIT License, refer to `license.md` for more information

# pylint: disable=missing-module-docstring
# pylint: disable=super-init-not-called

class InputError(Exception):
    """
        Raises an exception when some input value is not correct.
        Attributes:
            field - The input field where the error was encountered
            message - The explaination of the error and instructions
                for how to fix it
    """

    def __init__(self, field: str, message: str) -> Exception:
        self.field = field
        self.message = message
