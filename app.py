#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Part of XLSX to Odoo import
# Copyright 2020 David Todd <dtodd@oceantech.com>
# License: MIT License, refer to `license.md` for more information

"""
    A Really hacky script (not really), who's purpose
    is to import oddly formatted data that was provided
    on a customer pickup to data that the erp is
    expecting. This will accomplish the import via
    the XMLRPC interface
"""

import json
import itertools
from pprint import pprint

from openpyxl import load_workbook
from api import API

# Spreadsheet Stuff
SPREADSHEET = '<your spreadsheet>.xlsx'
SHEET = '<The Sheet name with the data>'
FIRST_ROW = 2 # Assumes that the actual first row is a header
LAST_ROW = 2064 # The last row that there is any data
LAST_COL = 6 # The last column to read from in each row

# Odoo Stuff
ASSET_CATALOG_ID = 3225 # The database ID of the asset catalog we are importing into
DATA_DESTRUCTION_ID = 1657 # The database ID of the data destruction we are importing into

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
            'children': [child.__dict__ for child in self.children if child is not None],
        })

class ProcessWorkbook:
    """
        Provides a mechanism for extracting the content
        from the workbook and uploading it to Odoo
    """

    def __init__(self):
        self.api = API()
        self.workbook = load_workbook(filename=SPREADSHEET, data_only=True)[SHEET]

        self.records = list()
        self.last_parent = None

        # These lists are expected to contain one or more Tuples
        # Each Tuple will be of the format (make, model)
        self.models_to_search = list()
        self.models_to_create = list()
        # The Tuples here will be of the format ((make, model), id)
        self.models_to_ids = list()
        print('Initialized ProcessWorkbook')

    def get_id_from_model(self, model):
        """
            Searches `self.models_to_ids` for
            a matching `model`, and returns the
            id if there is one. Returns None
            otherwise
        """
        for item in self.models_to_ids:
            if model == item[0][1]:
                return item[1]
        return None

    def serial_in_records(self, serial, records=None):
        """
            Determines if a particular serial number
            is in a record list, and returns True if so;
            otherwise, returns False

            `serial` is a string to check against the
            record list

            `records` is an optional argument that will
            search that specific record list (such as a
            parent's children) instead of just the parent
            records
        """
        if records is None:
            records = self.records
        if serial in [record.serial for record in records if record.serial]:
            return True
        return False

    def get_records(self):
        """
            Reads the workbook and sorts each row into
            multiple instances of the Record class.

            When this method comes across a "Parent"
            record, it stores that Record instance, which
            will be used whenever this method comes across
            a "Child" record.

            When this method comes across a "Child"
            record, it gets appended to the `children`
            list of the stored parent object.

            Returns `self` (this instance of ProcessWorkbook)
        """
        print('Getting rows from the spreadsheet and sorting relationships')
        for row in self.workbook.iter_rows(
            min_row=FIRST_ROW,
            max_col=LAST_COL,
            max_row=LAST_ROW
        ):

            serial = str(row[0].value)
            relationship = row[2].value

            if relationship == 'Parent':
                if not self.serial_in_records(serial):
                    record = Record(
                        serial = serial,
                        asset_tag = str(row[1].value),
                        make = str(row[3].value),
                        model = str(row[4].value),
                        device_type = str(row[5].value)
                    )
                    self.records.append(record)
                    self.last_parent = record

                    # Add unique models so we can search for their sellable ids
                    if record.model not in itertools.chain(*self.models_to_search):
                        self.models_to_search.append((record.make, record.model))

            elif relationship == 'Child':
                last_parent_children = self.last_parent.children

                if not self.serial_in_records(serial, last_parent_children):
                    record = Record(
                        serial = serial,
                        asset_tag = str(row[1].value),
                        make = str(row[3].value),
                        model = str(row[4].value),
                        device_type = str(row[5].value),
                        children = None
                    )
                    last_parent_children.append(record)

            else:
                pass

        return self

    def show_records(self):
        """
            Pretty Prints a JSON string for all
            of the records that are stored
        """
        pprint([record for record in self.records])

    def get_odoo_model_ids(self):
        """
            Iterates over unique models and searches
            Odoo for the database id of those models.
            Once the search is complete, `self.models_to_ids`
            contains a mapping between each unique model
            name and the database id.

            When a model can't be found, that model is printed
            so that a manual search can be done, or a new item
            can be created.

            When a model returns multiple ids, that model is
            printed so that a manual search can be done to
            select the "correct" database id.

            Returns `self` (this instance of ProcessWorkbook)
        """
        print('Searching Odoo for sellable items with matching models')
        for model in self.models_to_search:
            odoo_records = self.api.do_search_and_read(
                'erpwarehouse.sellable',
                [('model', 'ilike', model[1])]
            )

            if not odoo_records:
                print('Unable to find model: %s' % model[1])
                self.models_to_create.append(model)
            else:
                # If the search returns more than one, we'll
                # assume that it was the first one since some
                # models are duplicated (for whatever reason)
                self.models_to_ids.append((model, odoo_records[0]['id']))

    def create_missing_model_ids(self):
        """
            For any models that couldn't be located
            when initally searched, create them and
            then store those newly created ids

            Returns `self` (this instance of ProcessWorkbook)
        """
        print('Creating sellable items for missing models')
        for model in self.models_to_create:
            print('Creating model: %s' % model[1])
            result = self.api.do_create(
                'erpwarehouse.sellable',
                {
                    'make': model[0],
                    'model': model[1]
                }
            )
            self.models_to_ids.append((model, result))

        return self

    def create_line_items(self):
        """
            For all the records that we can
            process (there's a mapped model),
            create the asset catalog and
            data destruction line items.

            Returns `self` (this instance of ProcessWorkbook)
        """
        print('Creating Line items for accepted records in Odoo')
        for record in self.records:

            # Is the model one that we have the id for
            if self.get_id_from_model(record.model):
                result = self.api.do_create(
                    'erpwarehouse.asset',
                    {
                        'catalog': ASSET_CATALOG_ID,
                        'make': self.get_id_from_model(record.model),
                        'serial': record.serial,
                        'tag': record.asset_tag,
                    })
                print('Added id: %s' % (result))

                if not record.children:
                    device_type = '0'
                    if record.device_type == 'Network':
                        device_type = 'N'
                    elif record.device_type == 'Tape':
                        device_type = 'T'

                    result = self.api.do_create(
                        'erpwarehouse.ddl_item',
                        {
                            'ddl': DATA_DESTRUCTION_ID,
                            'make': self.get_id_from_model(record.model),
                            'serial': record.serial,
                            'storser': 'N/a',
                            'type': device_type,
                        }
                    )
                    print('Added id: %s' % (result))
                else:
                    for child in record.children:
                        device_type = '0'
                        if child.device_type == 'Hard Drive':
                            device_type = 'H'

                        result = self.api.do_create(
                            'erpwarehouse.ddl_item',
                            {
                                'ddl': DATA_DESTRUCTION_ID,
                                'make': self.get_id_from_model(record.model),
                                'serial': record.serial,
                                'storser': child.serial,
                                'type': device_type,
                            }
                        )
                        print('Added id: %s' % (result))
            else:
                print('Unable to add %s as there is no sellable id' % (record.serial))

        return self

    def run(self):
        """
            Runs everything in the order that is required
        """
        self.get_records()
        self.get_odoo_model_ids()
        self.create_missing_model_ids()
        self.create_line_items()

if __name__ == '__main__':
    ProcessWorkbook().run()
