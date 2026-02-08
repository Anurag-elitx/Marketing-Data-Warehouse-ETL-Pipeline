# Changelog

All notable changes to the Marketing ETL Pipeline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2026-02-09

### Added
- Centralized logging module (`src/logger.py`) with file and console handlers
- Configuration module (`src/config.py`) for centralized path management
- Comprehensive unit tests for KPI engine, merge logic, and ads ETL
- `CONTRIBUTING.md` with development guidelines
- `.gitignore` for Python projects

### Changed
- Refactored `main_etl.py` with proper error handling and timing
- Updated `requirements.txt` with pinned versions for reproducibility
- Added `load_ga4_data` function alias in `ga4_etl.py` for backward compatibility

### Fixed
- Function name mismatch between `main_etl.py` import and `ga4_etl.py` definition

## [1.0.0] - Initial Release

### Features
- Google Ads data ETL processing
- GA4 analytics data processing
- Data merging and KPI calculation
- Power BI dashboard integration
- Machine Learning models for ROAS and CPA prediction
- Budget optimization with Linear Programming
