# TO DEFINED A SPREADSHEET FOR DHIS2
[name_of_spreadsheet.csv](storage/resource/dhis2/name_of_spreadsheet.csv) (UTF-8 encoding) 

a new spreadsheet can be submitted via the menu Settings => DHIS2 Settings

new version 3 since march 2023

## CSV COLUMNS (keep order)

Fisrt line name of column (do not change this) :
dhis2_label;version;filter;type_sample;categorieoptioncombo;attributeoptioncombo;orgunit;storedby

dhis2_label : this label will be copied identically to the corresponding line in the result file

~~period : W for week or M for Month, must be present at least on the line after the header line~~ (useless from March 2023 in v3)

version : version number, v3, must be present at least on the line after the header line

filter : use to calculate, see below FILTER chapter or PREDEFINED KEYS

type_sample : serial corresponding to the type of sample in the database (cf table below) or 0, useful for calculate with the filter

categorieoptioncombo : will be copied identically to the corresponding line in the result file

attributeoptioncombo : will be copied identically to the corresponding line in the result file

orgunit :  will be copied identically to the corresponding line in the result file if empty the document header 1 will be used

storedby : will be copied identically to the corresponding line in the result file if empty the *FisrtnameLastname* of profile who does export will be used

## SYNTAX FOR FILTER

the operators =, !=, <, >, IN, AND ... must be preceded and followed by at least one space.

keyword OR : too complex and long request so the algorithm stops at the processing of the left part of the formula.

$_IDVARIABLE : Identifier of an analysis variable, see the details of an analysis using this variable from the analysis repository

$_IDVARIABLE = [NAME_OF_DICTIONARY.CODE] : selects the analyzes which one of the results corresponds to the indicated value

$_IDVARIABLE > NUMERIC_VALUE : selects the analyses which one of the results is higher than the NUMERIC_VALUE

$_IDVARIABLE = [NAME_OF_DICTIONARY.CODE] AND $_IDVARIABLE > NUMERIC_VALUE :
selects the tests where one of the results matches the indicated value and is greater than the NUMERIC_VALUE

$_IDVARIABLE IN ([NAME_OF_DICTIONARY.CODE1], [NAME_OF_DICTIONARY.CODE2], [NAME_OF_DICTIONARY.CODE3], ...) :
selects the analyses which one of the results corresponds to one of the indicated values

$_IDVARIABLE NOT IN ([NAME_OF_DICTIONARY.CODE1], [NAME_OF_DICTIONARY.CODE2], [NAME_OF_DICTIONARY.CODE3], ...) :
selects the analyses where one of the results does not correspond to the indicated values

{IDVARIABLE1, IDVARIABLE2, IDVARIABLE3, ...} : selects the analyses whose result contains one of the listed variables

CAT(SEX_M) : Selects the analyses in the records concerning male patients
CAT(SEX_F) : Selects the analyses in the records concerning female patients
CAT(AGE_1) : Selects the analyses in the records concerning the patients whose age is in the interval 1 (see age ranges settings in menu Settings => Age ranges)
CAT(SEX_M,AGE_2) : Selects the analyses in the records concerning male patients and whose age is in the interval 2

ON('CODE_OF_ANALYSIS1','CODE_OF_ANALYSIS2',...) : Selects the analyses whose code corresponds to this list 


## LIST OF SAMPLING TYPES

mysql> select id_data, label from sigl_dico_data where dico_name='type_prel';

| id_data | label                           |
|---------|---------------------------------|
|      34 | Liquide de ponction articulaire |
|      35 | Liquide de ponction ascite      |
|      38 | Biopsie                         |
|      50 | Crachat                         |
|      56 | Lavage Broncho Alvéolaire       |
|      75 | Prélèvement gorge               |
|      99 | Liquide Céphalo-Rachidien       |
|     100 | Liquide de ponction bronchique  |
|     102 | Liquide de ponction alvéolaire  |
|     104 | Liquide de ponction pleural     |
|     138 | Sang                            |
|     141 | Selles                          |
|     152 | Prélèvement urétral             |
|     153 | Urine                           |
|     162 | Prélèvement vaginal             |
|     163 | Autre                           |
|    1000 | Prélèvement génital             |
|    1014 | Eau potable                     |
|    1015 | Eau usée                        |
|    1016 | Eau de surface                  |
|    1189 | Prélèvement pus                 |

## LIST OF PREDEFINED KEYS FOR STATISTICS

The text in the column type_sample will be useless with predefined key

| key                            | period  | definitions                                                        |
|--------------------------------|---------|--------------------------------------------------------------------|
| NB_REC_SAVED                   | W or M  | Number of record with adminstrative status at least  in the period |
| NB_ANA_SAVED                   | W or M  | Number of analysis prescribed in the period                        |
| NB_SAMP_OUTSOURCED             | W or M  | Number of outsourced samples in the period                         |
| NB_STAFF                       | *none*  | Number of staff                                                    |
| NB_SECRETARY_TYPE              | *none*  | Number of secretary and advanced secretary                         |
| NB_TECHNICIAN_TYPE             | *none*  | Number of technician, advanced technican and qualitican techician  |
| NB_QUALITICIAN_TYPE            | *none*  | Number of qualitician and qualitician technician                   |
| NB_BIOLOGIST_TYPE              | *none*  | Number of biologist                                                |
| NB_EQUIPMENT                   | *none*  | Number of equipment                                                |
| NB_EQP_BREAKDOWN               | W or M  | Number of broken equipment in the period                           |
| NB_PROCEDURE                   | *none*  | Number of procedure                                                |
| NB_PRODUCT_WITH_EXPIRY_WARNING | *none*  | Number of product with expiry warning compared to the current date |
| NB_PRODUCT_WITH_EXPIRY_ALERT   | *none*  | Number of product with expiry alert compared to the current date   |
| NB_PRODUCT_UNDER_SAFE_LIMIT    | *none*  | Number of product under safe limit                                 |
| NB_PRODUCT_OUT_OF_STOCK        | *none*  | Number of product out of stock                                     |
| NB_OPEN_NON_CONFORMITY         | *none*  | Number of non conformity opened                                    |
| NB_NON_CONFORMITY              | W or M  | Number of non conformity (open and closed) in the period           |
| NB_INTERNAL_QUALITY_CONTROL    | *none*  | Number of internal control (even without result)                   |
| NB_INTERNAL_QUALITY_RESULT     | W or M  | Number of internal control results inthe period                    |
| NB_EXTERNAL_QUALITY_CONTROL    | *none*  | Number of external control (even without result)                   |
| NB_MEETING                     | W or M  | Number of meeting in the period                                    |

