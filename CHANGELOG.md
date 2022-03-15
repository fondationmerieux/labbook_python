# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
- Use code_var instead of id_data for sigl_07_data (variable of analysis)
- clean async process for import analysis repository

## [3.2.3] - 2022-03-10
### Added
- add second phone number
- display code patient in list-result page

### Changed
- remove spaces before to save phones
- when entering results, values of type x^n are formatted with n between 0 to 99
- nationality name are translated (FR/EN only)
- report : previous result are compared with date and time
- templates : add phone and phone2
- remove bill parts and bill button if bill module is disabled in preferences
- DHIS2 export with date ranges
- change user status int (29,30,31) by varchar (A,D,X)

### Fixed
- add number of analyzes in export of history of analyzes
- return status with listmedia and list achives
- insert equipment in DB
- syntax of age_unit in template QR code 
- user management, select prescriber when role is prescriber 
- some translations

## [3.2.2] - 2022-02-24
### Added
- QR code template to render a QR code image to insert into a specific report template

### Changed
- When entering results, values of type x^n are formatted with n between 1 to 9
- contact email for API page
- remove quality menu and no-conformity if quality module is disabled in preferences
- PDF report order of families depends of order of choice

### Fixed
- some translations
- remove grouped valdiation in technician profil
- pivot table some attribut are displayed by their labels instead of id (sex, type, status...)
- unit age by default are displayed on new patient form
- add a space between record number and record date on Bench sheet

## [3.2.1] - 2022-02-14
### Added
- add code patient search field in list of result and list of work pages
- add familly analysis search field in list of records and list of work pages
- new button for print one merge report of all reports validated in group mode
- display alert after login if an alert is present in the stock management
- zip code and city list setting
- api page with swagger-ui on your_labbook_url/sigl/api(Note: description of web services not finished) 
- add Internal and External control quality pages
- add manual about modify an odt template
- add to html template nonce attribute to inline script 
- add doc about import schemes

### Changed
- unoconv in listener mode instead of trying to generate a template after login
- redesign of user tables (1 table user, 1 table type of profil, no more id_group and id_role)
- modify alembic.ini and env.py to make the parameters variable
- Nationality use code instead of name
- every value of id_owner in DB are replaced by id_user instead of old id_group

### Fixed
- spelling error for minimal value in B008 analysis
- section in detail procedure not well displayed
- section in detail manual not well displayed
- multiple sample with code are saved

## [3.2.0] - 2021-12-15
### Added
- add pivot table
- new fields in patient details (middle name, nationality, resident, blood)
- possible to cancel stock move in history of a product
- new field description for dictionnary
- dependencies.md on github/doc
- new directory in /storage/resource/template
- template odt for report and stickers (code39 and qrcode format are avaible)
- code for pathological product (if not empty its used in WHONET export)
- test unoconv at first session run to preload

### Changed
- change size of code_patient column 8 => 20
- no choice anymore for validator with biological and technical validation
- remove quality menu for prescriber
- DB password can be customized via system
- orgunit and storedby are defined in v2 dhis2 spreadsheet
- popup notification changed
- INT to decimal(10,2) for cote_valeur in sigl_05_data
- drop more than 350 useless tables from DB

## [3.1.7] - 2022-01-26
### Fixed
- Empty biological validation page after a canceled result
- Security upgrade for Python to 3.9 and Pillow to 9.0.0

## [3.1.6] - 2022-01-12
### Changed
- New version number for generate new ISO

## [3.1.5] - 2021-12-10
### Changed
- New version number for generate new ISO

### Fixed
- In some template rename var value with tmp_value to avoid conflict

## [3.1.4] - 2021-11-17
### Changed
- email are clickable in pages : list doctors , list staff and list suppliers

### Fixed
- problem to display biological validation page when a empty answer in drown-down menu has been selected

## [3.1.3] - 2021-10-22
### Fixed
- delete first value in a dictionnary
- add strip for result value in Pdf report (bug with B258 by example)
- forbidden change on role of root
- stock management page in MG
- add translations for name of dictionnary too
- add redirection of error for alembic upgrade head in gunicorn.sh
- alembic upgrade 3.1.1, alter table convert wrong with multiple table in same request

## [3.1.2] - 2021-10-06
### Fixed
- bunch of translations
- search result in list-results page
- quote visible on few buttons
- text too long (with KM and LO) on homepage with Firefox

## [3.1.1] - 2021-09-23
### Changed
- No more validation step page for record request internal and external
- warning on record request if no sample

### Fixed
- english words works in search fields if english language is choose for repository
- few translations in dictionnary
- barcode generation (add Pillow library with pip)

## [3.1.0] - 2021-09-15
### Added
- New languages avaible : Arabic, Khmer, Laotian, Malagasy, Portuguese
- Add default language of laboratory in Pref settings (for IHM and Report)
- Add default language of analysis repository in Pref settings
- Add new column code lab in list of records

### Changed
- bold style for value out of range min/max
- way of selected language in user details

### Fixed
- number of emergency record

## [3.0.13] - 2021-08-30
### Fixed
- supply stock products

## [3.0.12] - 2021-07-15
### Fixed
- group validation
- error when creating a record with deleted analysis before saving
- move to labbook_BE directory ANALYZES.md, EPIDEMIO.md and DHIS2.md

## [3.0.11] - 2021-07-09
### Added
- ANALYZES.md
- EPIDEMIO.md
- DHIS2.md
- TABLES.md 
- Actions in Product catalog page

### Changed
- takes into account the users language
- title of E02 analysis

### Fixed
- import analysis repository, update variable too
- refresh table after creating a item
- blocks duplicate analyses in the same record
- export of stock
- switch data between two column of analysis repository table
- delete a product sheet 
- control on max use of a product if entered by keyboard

## [3.0.10 update] - 2021-06-28
### Added
- import status of the analysis repository

### Fixed
- PDF Multipage report 

## [3.0.10] - 2021-06-24
### Added
- new type of sample : Pus

### Fixed
- import analysis repository
- PDF Multipage report
- footer of PDF report
- search variable in details of analysis

## [3.0.9] - 2021-06-21
### Added
- Configurable epidemio page
- new sample analysis PB25

### Fixed
- rewritten PDF report function
- groups analysis families on PDF report

## [3.0.8] - 2021-06-10
### Added
- New analyzes B796, B797, B798, B799, B800, B801, B802, E06
- DHIS2 filter by Sex and/or Age
- DHIS2 filter on specific analysis 

### Changed
- restore and backup not synchronous anymore

### Fixed
- background stay grey in list-result page
- add popup wait for validation of internal and external request

## [3.0.7] - 2021-06-02
### Added
- initialization page wait for labbook_BE
- new ABG B659, B660, B661, B679, B680, B681
- Add Phenotype
- Code var for unique identifier (not finish)

### Changed
- DHIS2 reporting weekly
- SARS-CoV-2 analyzes modified
- Export WHONET with or without on analysis and variables

## [3.0.5] - 2021-05-05
### Added
- setting and export DHIS2
- import/export users

## [3.0.4] - 2021-04-22
### Added
- Analysis repository module
- csv export for report activity module

### Changed
- remove B171 analysis
- rename and add column in WHONET export 

### Fixed
- way for add and remove column for 3.0.2, 3.0.1 and 2.9.1

## [3.0.3] - 2021-04-14
### Added
- Ct unit
- 5 analyzes for SARS-CoV-2 (COVID 19) added

### Changed
- Non conformity module finished
- Paludisme and VIH formula modified for epidemio
- B136 formula modified
- size of column for analyzes codes

## [3.0.2] - 2021-04-01
### Changed
- No more PHP containers
- Storage management v2
- backup and restore module
- Delete B603 analysis

## [3.0.1] - 2021-03-09
### Added
- Patient management : details and combine records
- new icon qualitician and prescriber profils
- full translation

## [3.0.0] - 2021-02-26
### Added
- Quality : General / Laboratory / Staff / Prescribers / Equipment / Supplier / Manual / Procedure / Meeting
- Storage management
- Setting : Dictionnaries / Users / Age range / Stickers
- Reports : Epidemiology / Statistic / End of day / Daily invoice
- Patient history
- Analysis history
- Work list technician and biologist
- Status of current samples
- patient information in some title bar

### Fixed
- delete then add a analysis in external or internal pages fixed
- sort column
- hand icon cursor on head of column sortable
- popup when click on status of a record in list of record and list of work
- English translations

## [3.0.0-alpha.2] - 2020-12-17
### Changed
- List users
- Change password
- Disabled user
- Search user
- Setting Record number
- Setting Report
- Enable/Disable Billing
- Enable/Disable Quality

## [3.0.0-alpha.2] - 2020-12-17
### Changed
- List users
- Change password
- Disabled user
- Search user
- Setting Record number
- Setting Report
- Enable/Disable Billing
- Enable/Disable Quality

## [3.0.0-alpha.1] - 2020-11-01
### Changed
- Page login
- Homepage
- Preferences
- Logo

## [2.9.1] - 2020-10-20
### Added
- Migration of database with Alembic when Gunicorn is started
- Add admission date for internal request
- Add in DB 2*9 Antibiogramme (DISK and CMI method)
- Export WHONET in CSV file of [WHONET] Antibiogramme (B650 to B678)

## [2.9.0] - 2020-09-14
### Changed
- Final version of 2.9.0 branch validated

### Added
- Add Alembic, database migrations tool

### Fixed
- Patient details (age without birth date)

## [2.9.0-rc.2] - 2020-06-18
### Added
- Add popup waiting message for pages with filter by date
- Add popup confirm message for delete analysis in new record pages

### Fixed
- Optimize request for list of records page

## [2.9.0-rc.1] - 2020-06-05
### Added
- Automatic calculation on some type of result
- Automatic disconnection
- Previous result in PDF report
- Clinical information in PDF report

## [2.9.0-beta.6] - 2020-05-14
### Added
- Biological validation (missing previous result information)
- Technical validation
- PDF bill
- PDF report (missing previous result information)

### Fixed
- Limit range icon in enter-result, list-result, tech/bio validation
- Add yum install which to docker file (needed for pdfkit)
- information in popup history display

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
