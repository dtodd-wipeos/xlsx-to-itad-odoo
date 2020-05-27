# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.1] - 2020-04-06

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
