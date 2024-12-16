# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
- Use code_var instead of id_data for sigl_07_data (variable of analysis)
- clean async process for import analysis repository
- edit user able to upload file like CV, diploma ... as for edit staff GUI

## [3.5.0] - 2024-12-16
### Added
- internal messaging, quick access with envelope icon
- refresh every 30sec the number of unread messages

### Changed
- css redesign of header banner

### Fixed
- user-info block displayed when language is read from right to left

## [3.4.11] - 2024-09-09
### Fixed
- API and Lab profile was blocked
- Incorrect billing calculation with reduction if an analysis is deleted via the administrative record  

## [3.4.10] - 2024-07-29
### Fixed
- security fix
- Daily billing report when more than 50 bills

## [3.4.9] - 2024-07-08
### Changed
- Laotian translations
- New FMX logo in contributors page

### Fixed
- export WHONET
- loaded patient age unit
- age unit cannot be registered empty
- export of report today

## [3.4.8] - 2024-06-26
### Fixed
- start and end dates for pages : det-hist-analysis, global-report, hist-analyzes, hist-stock-product, user-conn-export, report-activity
- calculation for TAT report when validation technical is in the same minute of record save
- stock moved
- default unit_age for patient form

## [3.4.7] - 2024-06-24
### Changed
- patient age required

### Fixed
- old patient variables names for banner
- added the latest translations
- searches with a date field
- testing document templates
- activity report with age in days, weeks or months
- calculation for TAT report
- list of civilties from database in pages setting-det-user, det-staff and det-doctor
- bug after moving stock without changing the quantity

## [3.4.6] - 2024-06-17
### Added
- parameter to indicate whether an analysis is of type AST
- dry run mode for send data to DHIS2 API

### Changed
- displayed interval with seconds for TAT

### Fixed
- rec_date format with new record from API
- formula with pattern {id_var, id_var2, ...} for DHIS2

## [3.4.5] - 2024-05-15
### Added
- upload customizable form patient by TOML file, see customizable_form.md
- Numerical result converted can be add to PDF report with res.valueConv and res.unitConv (empty if no conversion formula)

### Changed
- send data to DHIS2 API, displayed return message from platform even for success
- add var_formula_conv, var_unit_conv, var_accu_conv in import/export analysis repository, version v4

### Fixed
- rec_date conversion of API Record service
- algorithm for dhis2, epidemio report and indicator report
- bug with filename of WHONET export
- a look back at the use of current_app in db.py

## [3.4.4] - 2024-04-04
### Added
- DHIS2 API settings
- button to send data to DHIS2 API in export DHIS2 page

## [3.4.3] - 2024-03-26
### Added
- Redesigned equipment GUI
- Turn Around Time report, add record number as filter
- Turn Around Time report, add technical time as column
- Turn Around Time report, add result time as column

### Changed
- Turn Around Time report, calculation changed

### Fixed
- previous result displayed even if from the same day
- calculation for indicator, dhis2, epidemio reports
- display min or max if only one of them
- Record via API, fixed problem with prescriber
- Record via API, rec_invoice_discount doesnt display label in administrative page
- Record via API, add enum to pat_sex
- Record via API, add a default pathological product associated with the analysis if doesnt exist in the data received
- accuracy of numerical results can be converted into another unit.

## [3.4.2] - 2024-02-20
### Added
- Turn Around Time report
- Numerical results can be converted into another unit. Enter the conversion formula in the analysis repository. 
(Example if you want multiply the value by 1000, write : $ * 1000)
- New type of profile for api access
- Possibility to create a new record via API

### Changed
- new text and logos in contributors page

### Fixed
- the display of min and max values can be forced for technical and biological validation

## [3.4.1] - 2024-01-11
### Added
- new filter AGE for DHIS2 (see documentation dhis2.md) 
- new system for recording biological validation comments
- recording the date of administrative validation of a file, (for template use o.rec.rec_date_save)
- the display of min and max values for the results screen can be forced
- displays last previous result to date for enter-result and list-results pages

### Fixed
- Indicator formula can use keyword OR, same sample_type for both part of formula

## [3.4.0] - 2023-12-28
### Added
- hl7apy library
- UI and DB table for setting analyzer
- Icon for Connect in admin homepage
- name and firstname of patient for pivot table
- rec_num_int in result and analysis dataset for pivot table
- In the details of an analysis variable, a button to obtain the dictionary details of the type of results
- a critical new feature for suppliers

### Changed
- upgrade python-barcode
- UI for specimen in record request (link to analysis and no more quantity)
- new background image on login page
- forced to choose a type of sex for patient form
- instead of period (year of mont/year) we displayed date of record next to record number
- change few columns date to datetime (rec_parcel_date, samp_date, samp_receipt_date)
- increases the report download counter for group validation and global reports
- DHIS2 spreadsheet can use keyword OR (be careful calculation could be long !)

## [3.3.16] - 2023-11-07
### Changed
- rename 17 tables
- deleted 15 unused tables

### Fixed
- add staff by quality menu 

## [3.3.15] - 2023-10-06
### Fixed
- rebuild ISO and retry to create manual_setting table by Alembic

## [3.3.14] - 2023-09-27
### Fixed
- status of last import of analysis repository
- export WHONET variables when "Diam. inhibition" missing then looking for "... inhibition diam."

### Changed
- logo AEGLE
- Minor changes in documentation concerning restores and upgrade

## [3.3.13] - 2023-07-21
### Changed
- system enhancement insertion of an analysis variable for code_var

### Fixed
- move stock more than one item
- move stock when split number of pack

## [3.3.12] - 2023-07-13
### Added
- stock setting add location stock
- location fields in supply of product becomes a drop-down menu
- location of stock product can be changed to another location
- stock supply can be split to another location
- hospital identification to WHONET export

## [3.3.11] - 2023-07-11
### Fixed
- some translations with double backslash n, one backslash missing
- stock setting

## [3.3.10] - 2023-07-06
### Fixed
- some translations with double backslash n, one backslash missing

## [3.3.9] - 2023-07-05
### Added
- analysis commentary variable for pdf report, ana_comm (like var_comm)
- laboratory profil (can only read and export quality sections) 
- identification number field for internal request (rec_hosp_num)
- GUI for view procedure downloads (Admin and Qualitician) 
- add category (configurable) for manual

### Fixed
- indicator.ini replace CAT_H => CAT_M (Labbooks already installed to be corrected manually)
- short cut for edit user able to upload file like CV, diploma ... as for edit staff GUI

## [3.3.8] - 2023-05-04
### Added
- testing function for import analysis repository
- added a new user without access, with staff role
- trace in DB when a procedure is downloaded (new trace_download table)
- concat prescriber title (if exist) with prescriber_name for PDF report

### Changed
- reference to "Cancels and replaces" if a report already exists and the file has been modified (= cancel or reset value) 
- rewriting import.md
- add right to stock manager profil to edit and delete suppliers
- update Pipfile packages (see dependencies.md) 
- only biologist profile can delete a record

### Fixed
- user setting add new doctor button displayed
- vertical scrollbar in menu in desktop mode if they need
- redundancy of the name of the biological validator in the report
- add Spanish in choice of locale in details of user
- wrong count of product in stock if an used product was canceled

## [3.3.7] - 2023-04-17
### Added
- default indicator.ini
- new default spreadsheet for statistic in DHIS2
- in list template setting added test on menu for outsourced template

### Changed
- if a record has 2 analyses with 2 different functionnal unit, we add up comment and validator on report

### Fixed
- syntax error for details of stock on treatment of prs_expir_date
- dhsi2 key NB_OPEN_NON_CONFORMITY was wrong count
- upload procedure, external control, manual, meeting, staff and equipment

## [3.3.6] - 2023-04-05
### Added
- note on the keyword OR in dhis2.md

### Changed
- in setting analyzes disabled or enabled all analyzes except sample acts
- stock setting is allowed for the stock manager profil too

### Fixed
- no more empty result displayed in report
- menu in small viewport add a scroll to see the bottom items

## [3.3.5] - 2023-03-16
### Added
- new predefined DHIS2 export for outsourced samples
- add some predefined keys for DHIS2 export (new version 3)
- custody application choice in external test request
- add patient sex, phone1, phone2 in dataset Result, Record, Analysis for pivot table 
- display internal record number if exist under other number in list of records and list of works
- possibility to update clinic information after administrative validation

### Changed
- change settings of DHIS2
- update dhis2.md
- responsive patient details GUI

### Fixed
- missing date backup status except in admin profil
- replace history.back in some pages (like edit product details)
- filter of list of record and list of work pages with pofil in functionnal unit
- delete a pathological product in a record
- refresh bill price and remain after del an analysis in an administrative record
- some buttons of non-conformity GUI were disabled
- the expiration date of a product was badly managed if it was not mandatory
- problem with update of stock setting 

## [3.3.4] - 2023-02-28
### Changed
- gunicorn logs, Front-end and Back-end logs have been moved in logs
- Add some form fields can be enabled or disabled
- Functional units are active on analysis search 
- cancel and replace date on report is the date of previous report
- Undo : More control over numeric result fields
- export dictionnary order by dico_name

### Fixed
- add stock product, wrong insert
- display none overstepped by d-*-flex, like in detail patient with anonymous function
- download indicator.ini
- lastname and firstname filters in patient history page 
- add_analysis function, outsourced parameter missed
- empty report if an analysis is with a labeled variable at first position
- focus on search field supplier of det-new-product page

## [3.3.3] - 2023-02-08
### Added
- Functional unit active in the pages list-records, list-works, list-results and list-samples
- Indicator page (see indicator.md)
- The obligation of the expiration date of a product supply is configurable
- Some form fields can be enabled or disabled
- Page list of analysis variables
- add formatting option on dictionnary details to display in report if your template use it
- possible to indicate that an analysis is outsourced
- outsourced template (test version)

### Changed
- More control over numeric result fields
- took off new catalog reference because is redondant with supplier reference
- pages : login, homepage, list-result and enter-result are responsive on smartphone
- numerical results are rounded to the precision defined in the analysis repository

### Fixed
- redirect on homepage after edit user details or password via menu
- product supply
- display no result alert if no result to print for global report
- import / export dictionnary (import doesnt removed dictionnary, only add and update)

## [3.3.2] - 2023-01-12
### Added
- filter by lessor name in list of stock page

### Changed
- import/export analysis repository in V4 without formula2, unit2 and accu2 

### Fixed
- search field analysis

## [3.3.1] - 2023-01-10
### Added
- added profile dedicated to stock management
- functional unit associated with users and analysis families
- name of lessor in product details
- catalog reference in porduct details
- customizable alert duration
- export csv of supplies and uses products becomes a table with history
- set up a list of requesting services
- delete a analysis in a record between administrative validation and technical validation
- more filters in patient history page
- admin can disabled/enabled all analyzes
- possible to import/export dictionnary
- filter by analysis in list of result page
- filter requesting services in statistic report page

### Changed
- biologist can download an original PDF report or a duplicate after 1st download
- in details equipment textarea of breakdown and maintenance
- Possibility to reset or cancel a result after a technical validation
- Possibility to reset a result after a biological validation
- time after cancel and replace sentence in report
- Add in bold the fields of type_result free as a subtitle
- more data (title, samples... for template report)
- expiration date can be not mandatory in product supply
- quotation of all sampling procedures at 0
- no more formula 2 in analysis details

### Fixed
- Result and Analyzes dataset for pivot table
- delete duplicate of type_result in dictionnary table
- filter type of record in list of records page

## [3.3.0] - 2022-12-15
### Added
- user can changed his own profil and password
- for pivot table in all dataset add birth, age, age_unit, doctor_lname and doctor_fname
- last backup information on homepage
- custody application choice in impatient test request
- after dowloading a record report for the first time, duplicates will be available for download afterwards
- download a global PDF of merge reports between 2 dates
- highlight setting for result of analysis variable (show only in report if template use it)
- record validation date avaible for report templates
- datetime of cancel and replace report avaible for report templates
- internal laboratory record number
- in list of record add type of record filter

### Changed
- no more Please reconnect message but force redirect to login page
- more details displayed in search patient field

### Fixed
- Almost all GUI (85 files) because of change to Bootstrap 5
- add popup wait when deleting something

## [3.2.15] - 2022-11-02
### Fixed
- problem with filter CAT(SEX_,AGE_) in DHIS2 export
- update Pillow library

## [3.2.14] - 2022-10-18
### Fixed
- changed role of an user

## [3.2.13] - 2022-09-29
### Fixed
- conversion to missing string when age is in months or days
- corrects the age in months sometimes different with the report

## [3.2.12] - 2022-07-26
### Fixed
- Do not allow the price of the act to empty put minimum 0
- corrects a calculation problem for analyzes with formulas presented several times in the result entry list

## [3.2.11] - 2022-07-12
### Fixed
- when 3 or more analysis with same familly follow then the familly name is repeated on report

## [3.2.10] - 2022-06-22
### Fixed
- page stock details displayed wrong sum of pack after a cancellation

## [3.2.9] - 2022-05-19
### Changed
- delete link with var for PB7

## [3.2.8] - 2022-05-09
### Fixed
- search an user in user list
- after cancelled a supply product, it was still display in detail of this product
- upload template

## [3.2.7] - 2022-04-27
### Changed
- changes the values for timeout : listmedia and listarchive 3min => 6min, backup 15min => 5h, restore 20min => 25h 
- download file in a new tab

### Fixed
- problem with canceled a product supply 
- search with code or code lab in historic patient page
- Laotian correction
- Sex of patient added in record dataset for pivot table

## [3.2.6] - 2022-04-11
### Fixed
- report with analyzes that dont have a familly (expl : B506)
- origin column in setting users page
- During a biological validation if you uncheck an analysis then it wont be in the report.

## [3.2.5] - 2022-04-07
### Added
- display id of user in a column for list of users

### Changed
- Report and Sticker PDF are in PDF/A-1 (ISO 19005-1:2005) instead of PDF 1.5
- name of column Manual to Procedure for list of procedure
- secretary (advanced too) are forbidden to edit or delete a non conformity
- new supplier open in a other tab for product details page
- no more default date in DHIS2 export page

### Fixed
- problem to compare value to min or max if value is like 10^n
- when download a file we check if file exist and size > 0 if not redirect on current page
- if we add an new analysis post biological validation the new validation reedit report with Cancel and Replace text
- during a second biological validation, display the previous comment
- display phone 1 and phone 2 on administrative record page
- export stock if one fields is null
- convert value of impact_patient and impacts_perso_visit from sigl_non_conformite_data (4,5,6,7) to (1053,1055,1057,0)

## [3.2.4] - 2022-03-30
### Added
- in pivot table add result_unit and label of result_value and an_emergency
- add trim to every textarea values
- display count of download report file
- add step="60" for input datetime-local, thats forced time in HH:MM
- report data object for template : o.report.replace, o.rec.num (num_rec_y or num_rec_m depends of setting)

### Changed
- reedit of report generate a new report not overwriting on the existing
- 29 unused tables deleted still 11 tables on 82 unused but not yet deleted

### Fixed
- patient dataset, problem with jointure on pat_nation, pat_blood_group and pat_blood_rhesus
- regex x^n fixed for n > 9 in enter-result page
- technical and biological validations were without time, added time in date selectors
- DHIS2 export with date ranges and refactoring period
- save details of an user
- WS ScriptStatus if file doesnt exist or empty
- multi line comment in report pdf for record, variable analysis and biological validation comment

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
- Add default language of laboratory in Pref settings (for GUI and Report)
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
