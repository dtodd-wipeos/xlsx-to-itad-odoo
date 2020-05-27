# XLSX to Odoo import

The goal of this program is to parse a spreadsheet (in a particular format from one of OceanTech's customers)
and then load that parsed data into and Odoo instance that has the ITAD module.

This uses a "library" of sorts that I created for various projects that involves communicating with an Odoo instance.
The library is found in `api.py` and `exceptions.py`, and supports full CRUD actions.

The types of records that are created are:

* Sellable Records - These are records that form the basis of our "inventory". They contain basic information such as make and model, as well as reimbursement values
* Asset Catalog Lines - These records are what appear in the asset catalog table. Each one is a line item
* Data Destruction Lines - These records are what appear in the data destruction table. Each one is a line item

## Version

The current version is 1.1.1. Please check changelog.md for more information.

## Usage

This was designed to parse a very specific spreadsheet, and may work on others that are similar in layout.
The ideas within this application should be able to be adapted towards processing other spreadsheets.

1. Clone this repo
1. Ensure that you have [Pipenv](https://github.com/pypa/pipenv) installed
1. Install the [openpyxl](https://bitbucket.org/openpyxl/openpyxl/src/default/) dependency - `pipenv install`
1. Edit `run.sh` to point to your Odoo instance, with credentials that can search and create ITAD records
1. Edit `app.py` and modify the constants (all capital letters) at the top to reflect your spreadsheet and Odoo configuration
    * Spreadsheet configuration includes: Filename (relative or absolute), the Sheet to work from, as well as the rows and columns to fetch
    * Odoo configuration includes: Asset Catalog ID and Data Destruction ID. These are both the database ids of their respective forms. Used to connect the line items to specific records
    * `SERIALS_TO_IGNORE` specifies a list of serial numbers to not check for duplicates and to always create new records
6. Enter the virtual environment - `pipenv shell`
1. Start the application - `./run.sh | tee output.log` - This can take a couple minutes depending on how big the spreadsheet is