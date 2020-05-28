#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Part of XLSX to Odoo import
# Copyright 2020 David Todd <dtodd@oceantech.com>
# License: MIT License, refer to `license.md` for more information

# pylint: disable=import-error

"""
    Provides the Record class, which is a close
    representation of an Odoo Record for the purposes
    of importing line items.
"""

import json

class Record:
    """
        Stores information about the line items to import.

        All fields but one are expected to be of type `str`,
        and this class will enforce that when an instance is created.
        The only field that is not expected to be a string is
        the `children` field, which should be a list containing
        one or more Record objects, or None
    """

    def __init__(self, **kwargs):
        self.serial = str(kwargs.get('serial'))
        self.asset_tag = str(kwargs.get('asset_tag'))
        self.make = str(kwargs.get('make'))
        self.model = str(kwargs.get('model'))
        self.device_type = str(kwargs.get('device_type'))

        self.children = kwargs.get('children', list())

        # Special case for serial numbers recorded as dell links
        if 'dell.com' in self.serial:
            # We assume that there are no '/' characters in the serial,
            # and that the serial is the very last thing in the link.
            # For dell, this is fine, as they are sturctured like:
            # https://qrl.dell.com/H6FND42
            self.serial = self.serial.split('/')[-1]

    def __str__(self):
        """
            Returns the serial number of this Record instance
        """
        return self.serial

    def __repr__(self):
        """
            Used when iterating over a list of Record objects

            Returns a JSON serialized string that
            represents this Record. Children will be
            represented as a list of dictionaries or
            `null`
        """
        return json.dumps({
            'serial': self.serial,
            'asset_tag': self.asset_tag,
            'make': self.make,
            'model': self.model,
            'device_type': self.device_type,
            'children': [
                child.__dict__ for child in self.children
                if child is not None
            ] if self.children is not None else None,
        })
