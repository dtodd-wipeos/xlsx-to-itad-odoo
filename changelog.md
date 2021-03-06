# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.3] - 2020-06-04

### Changed

- All methods have had [python type hints](https://www.python.org/dev/peps/pep-0484/) added
- Documentation has been updated to include these type hints, and links to github commits

## [1.2.2] - 2020-06-04

### Added

- Dependency for [pdoc3](https://pdoc3.github.io/pdoc/) to allow documentation generation from docstrings
- Script to generate the documentation (apparently any needed environment variables for normal operation have to be defined)

### Changed

- Configuration options have moved (again!) to `config.sh`. I don't have intentions of moving it again, but we'll see.

## [1.2.1] - 2020-05-29

### Changed

- Log files generated by this program will now be in the same directory, rather than `logs/` (which the program didn't check if it existed)
- The `remove_ignored_records` method has been tweaked to be slightly more efficient (removed one loop as there was already another one there)

## [1.2.0] - 2020-05-28

### Added

- Saving of "Serials to Ignore" to a CSV file. This is used to select lines that shouldn't be imported, but do need to be looked at carefully
- The number of rows being processed is kept track of and reported at the end of the program
- CSV files generated as a result of this program are now ignored in git
- We now keep track of the number of each type of record uploaded
- We now track instances of failed records and see the data. Normally when a record fails to be created, it is due to being a duplicate.

### Changed

- Asset lines are now checked to see if they exist in Odoo before blindly creating new records (Asset Catalog only. This is not currently on the data destruction)
- Record objects are now able to be duplicated for cases of "Serials to Ignore" (Multiple Records with the same "Serial Number")
- The Print statements have been replaced with native logging, which output to STDOUT and a file
- Configuration of this program has been moved to `run.sh`. You should not need to alter `app.py` going forward.
- The Record class has been broken out into its own file, to help with readability

## [1.1.1] - 2020-05-27

### Added

- Automatic linting when a PR for master is created using alpine-pylint docker container

### Removed

- Private method `_set_device_type` has been removed, and folded back into `_create_data_destruction_line`

## [1.1.0] - 2020-04-06

### Added

- SERIALS_TO_IGNORE constant to skip checking for duplicate serial numbers

### Changed

- ASSET_CATALOG_ID and DATA_DESTRUCTION_ID constants may now be set to None. When either is None, that form will be skipped
- Relationship is no longer necessary to create records (such as just an asset catalog). It's previous behavior is the same if the Relationship is set

### Deprecated

- `get_records` has been renamed to `build_record_list` and simplified. A `get_records` wrapper is available that prints a warning and runs `build_record_list`

## [1.0.0] - 2020-04-01 - Initial Release
