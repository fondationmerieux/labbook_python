# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
- Biological validation
- PDF bill
- PDF report
- Automatic calculation on some type of result (11 / 704) 
- Automatic disconnection
- Top menu

## [2.9.0-beta.5] - 2020-04-30
### Fixed
- Storage information missing in DB (need for upload)

## [2.9.0-beta.4] - 2020-04-28
### Added
- Delete action in list of records 
- Upload a file to a record
- Technical validation (In Progress)

### Fixed
- Delete a document file administrative-record page
- Download a document file administrative-record page
- Display and download report file in administrative-record page

## [2.9.0-beta.3] - 2020-04-15
### Added
- Display history information of record in list result
- Add new analysis request in enter-result page
- Save & load result in page enter-result and list-result
- Finish editing contributors page

### Fixed
- Automatic billing calculation in new request pages
- take into account the hospital billing preferences in New External request page
- No more samples section in New External request page
- Limit min & max on values in result pages
- Button Save (result) enabled when someone focus at least one result box
- Generate a barcode image (need to include in a PDF file)
- Load files in administrative-record page (link not active)

## [2.9.0-beta.2] - 2020-03-30
### Added
- Share server host via cookies
- Generate a patient code
- Display of Record number according to preferences
- List of result (no savings result)
- List records : action to enter result
- library python-barcode
- library pdfkit
- footer page php and python same number
- contributors : url site labbook changed

## [2.9.0-beta.1] - 2020-03-20
### Added
- List records
- New External request
- New Internal request
- List of result [In progress]
- Contributors page
- Skeleton of HTML pages
- Various webservices with DB requests
