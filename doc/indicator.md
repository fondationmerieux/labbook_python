# TO DEFINED A CONFIG FILE FOR INDICATOR REPORT
The [indicator.ini](storage/resource/indicator/indicator.ini) file must be present and compliant (UTF-8 encoding)

In administrator access you can override the indicator.ini file, to know you have to keep the same file name

# TO DEFINE A CONFIG FILE FOR INDICATOR REPORT

The [indicator.ini](storage/resource/indicator/indicator.ini) file must be present and compliant (UTF-8 encoding).

With administrator access you can override the `indicator.ini` file, but you must keep the same file name.

**Current version:** 2 (since 18/06/2026)

## Version history

### v2 (18/06/2026)
- Clarified formula syntax requirements.
- Variables must be used in a complete expression (e.g. `$_284 > 0` or `$_256 = [posneg.+]`).

### v1 (17/04/2023)
- Initial version.

---

## [SETTINGS] section
- **version** : version number  
- **nb_disease** : number of diseases defined  

If `nb_disease = 4`, then sections `[DISEASE_1]` to `[DISEASE_4]` must be defined.

---

## [DISEASE_xxx] section
- **disease** : label of disease  
- **sample_type** : list of serials corresponding to the type of sample in the database (see *List of Sampling Types* below).  
  Even for a single serial, you must write it as a list: `[my_serial]`.  
  This field is only used for display, not for formula evaluation.  

- **nb_res** : number of results to display  

If `nb_res = 4`, then the following must be defined:  
`res_label_1` to `res_label_4`, `formula_1` to `formula_4`, and `sample_type_1` to `sample_type_4`.

- **res_label_xxx** : label of result to display  
- **formula_xxx** : calculation formula for the result.  

  **Important:** The syntax of formulas is the same as described in the DHIS2 filter documentation.

  - A variable must always be used in a complete expression.
  - Valid examples:
    - `$_284 > 0`
    - `$_256 = [posneg.+]`
    - `$_614 IN ([especepalu.pl_falc], [especepalu.vivax])`
    - `{106}`
  - Invalid example:
    - `$_284

  - **How many entries in `sample_type_xxx`: count the `AND` and the `OR` of the formula, then add 1.**
    Each part of the formula consumes one entry, taken in order, so repeat the same serial when the
    parts share a sample type.  
    - `$_284 > 0` : no operator, so 1 entry, `[138]`  
    - `$_7 >= 0.7 AND $_7 <= 1.4` : 1 operator, so 2 entries, `[138,138]`  
    - `$_7 >= 0.7 AND $_7 <= 1.4 OR $_7 >= 0.6 AND $_7 <= 1.1` : 3 operators, so 4 entries, `[138,138,138,138]`  
  - Too few entries and the indicator fails to compute, with `IndexError` in the log.  
  - If `formula_xxx` is empty, then `res_label_xxx` will be considered as a separator title and `sample_type_xxx` is not required.  

- **sample_type_xxx** : serial corresponding to the type of sample used in the formula.  
  Even for a single serial, you must write it as `[my_serial]`.

---

## LIST OF SAMPLING TYPES

```sql
mysql> select id_data, label 
       from sigl_dico_data 
       where dico_name='type_prel';

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
