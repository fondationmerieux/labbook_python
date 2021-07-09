# TO DEFINED A SPREADSHEET FOR DHIS2
[name_of_spreadsheet.csv](storage/resource/dhis2/name_of_spreadsheet.csv) (UTF-8 encoding) 

a new spreadsheet can be submitted via the menu Settings => DHIS2 Settings


## CSV COLUMNS

Fisrt line name of column (do not change this) :
dhis2_label;period;version;filter;type_sample;categorieoptioncombo;attributeoptioncombo

dhis2_label : this label will be copied identically to the corresponding line in the result file

period : W for week or M for Month, must be present at least on the line after the header line

version : version number, v1, must be present at least on the line after the header line

filter : use to calculate, see below FILTER chapter

type_sample : serial corresponding to the type of sample in the database (cf table below) or 0, useful for calculate with the filter

categorieoptioncombo : will be copied identically to the corresponding line in the result file

attributeoptioncombo : will be copied identically to the corresponding line in the result file


## SYNTAX FOR FILTER

the operators =, !=, <, >, IN, AND ... must be preceded and followed by at least one space.

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
+---------+---------------------------------+
| id_data | label                           |
+---------+---------------------------------+
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
+---------+---------------------------------+
21 rows in set (0.00 sec)
