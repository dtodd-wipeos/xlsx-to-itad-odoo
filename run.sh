#!/bin/bash

# Sets up the environment and runs the script

# Odoo Connection settings
export odoo_host='https://erp'
export odoo_database='OceanTech'
export odoo_user=1
export odoo_pass=''

# Odoo Records - These are the database ids of the records that contain the table/list
export odoo_asset_catalog_id=0
export odoo_data_destruction_id=0

# Spreadsheet configuration
export spreadsheet='<path to your spreadsheet>.xlsx/xlsm'
export sheet='<The Sheet name with the data>'

# Assumes the actual first row is a header
export first_row=2
# The last row there is any data we care about
export last_row=2000
# The last column that we care about
export last_col=6

# Serials to ignore are special cases that we should skip that line item
# One per line.
export serials_to_ignore=$(cat << EOF
N/A
EOF
)

python3 app.py
