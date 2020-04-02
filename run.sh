#!/bin/bash

# Sets up the environment and runs the script

export odoo_host='https://erp'
export odoo_database='OceanTech'
export odoo_user=1
export odoo_pass=''

python3 app.py
