# List of possible imports into LabBook

## Analysis repository
List of columns and theirs types of datas

version          : v3
id_ana           : integer, 0 for a new analysis (only in add mode) else if > 0 update analysis (in update mode) or insert analysis (in add mode if this id is not already taken by another analysis)
id_owner         : integer, 0 or id of user
ana_code         : string, unique code per analysis, (max 7 characters)
ana_name         : string (max 120 characters)
ana_abbr         : string (max 20 characters)
ana_family       : integer, 0 (without family) or id_family
ana_unit_rating  : string (max 2 characters)
ana_value_rating : float
ana_comment      : string
ana_bio_product  : integer, 0 (without sampling act) or id_product
ana_sample_type  : integer, 0 (without type of specimen) or id_specimen
ana_type         : integer, 0 or 170 (individual) or 171 (combined, 21/04/2023 useless)
ana_active       : Y or N
ana_whonet       : Y or N
id_link          : integer, 0 (only in add mode) or id_link
link_ana_ref     : integer, 0 for a new analysis (only in add mode) else if > 0 update analysis (in update mode) or insert analysis (in add mode if this id is not already taken by another analysis)
link_var_ref     : integer, 0 or empty if analysis without variables
link_pos         : integer, display position of this variable
link_num_var     : integer, useful for analysis with calculation fields
link_oblig       : Y or N, with Y this result will be mandatory
id_var           : integer, id of variable
var_label        : string (max 120 characters)
var_descr        : string (max 120 characters)
var_unit         : integer, 0 or id_unit
var_min          : float
var_max          : float
var_comment      : string
var_res_type     : integer, 0 or id_res_type
var_formula      : string
var_accu         : integer, precision is used on integer or real results
var_code         : string, unique code per variable, (max 10 characters)
var_whonet       : Y or N
var_qrcode       : Y or N
var_highlight    : Y or N, allows us to highlight this result in the report

### In the "Update analyses (with identical code)" mode

Look if the code of the analysis already exists in the database:
- an error in the search => an error that will be displayed the GUI in the "status of the last import"
ERR;AnalysisImport ERROR SQL verify code analysis code=with_the_code_of_the_analysis

- this code does not exist => it moves to the next row of the csv

- the code exists => it updates the analysis part (table sigl_05_data) then it retrieves the list of associated variables (table sigl_05_07_data) for
if the "id_refvariable" is identical it updates the info of the variables (table sigl_07_data) and the info specific to the link with this analysis (whonet, qrcode, position... cf table sigl_05_07_data)
But it doesn't remove a link with a variable nor add a new one.

This mode is only to update information, not to modify the structure of your repository. So no deletion or creation.

### In the "Add new analyses (code not existing in the database)" mode

Look if the code of the analysis already exists in the database:
- an error in the search => an error that will be displayed the GUI in the "status of the last import"
ERR;AnalysisImport ERROR SQL verify code analysis code=with_the_code_of_the_analysis

- this code exists => it goes to the next row of the csv

- this code does not exist => add the analysis (table sigl_05_data), look if the id_link is > 0 [there is perhaps a problem of principle]
if ok then look if the associated variable already exists thanks to the following characters (libelle, type_result, unite, normal_min, normal_max, code_var)
if the variable exists we get its id to link it with the analysis
if the variable does not exist then we add it (table sigl_07_data)
last step we link the analysis with the variable (table sigl_05_07_data)

At the end of the process a verification of the ghost variables (not present in the table sigl_05_07_data) in order to delete them.

## Dictionnary
List of columns and theirs types of datas

version         : v1
id_data         : integer, 0 (serial) or serial (update)
id_owner        : integer, 0 or id of user
dico_name       : string (max 20 characters)
label           : string (max 255 characters)
short_label     : string (max 20 characters)
position        : integer
code            : string (max 10 characters)
dico_descr      : text
dict_formatting : Y or N, allows us to highlight this value of result in the report

## Users
List of columns and theirs types of datas

version         : v3, (since 21/04/2023 v3.3.8, version move to first column)
firstname       : string (max 50 characters)
lastname        : string (max 50 characters)
username        : string (max 50 characters)
password        : encrypted string (max 81 characters)
title           : integer, 0 or id_title
email           : string (max 200 characters)
status          : A or D, A=Activated, D=Disabled
locale          : string, FR / UK / US / ES / AR / KM / LO / MG / PT
cps_id          : string (max 30 characters)
rpps            : string (max 11 characters)
phone           : string (max 20 characters)
initial         : string (max 5 characters)
birth           : yyyy-mm-dd
address         : text
position        : string (max 50 characters)
cv              : text
diploma         : text
formation       : text
darrived        : yyyy-mm-dd
deval           : yyyy-mm-dd
section         : integer, 0 or id_section
comment         : text
side_account    : integer, 0 or id_prescriber
role            : string (max 10 characters)

## Zip code and city
List of columns and theirs types of datas

zip_code  : string
city_name : string


> Note :
>
> - UTF-8 encoding
> - First row as column heading
> - Keep the columns in the same order
> - The syntax of columns must be identical
