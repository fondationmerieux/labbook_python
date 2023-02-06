# List of possible imports into LabBook

## Users
| firstname | lastname | username  | password         | title   | email   | status  | locale | cps_id  | rpps   | phone  | initial | birth      | address | position | cv     | diploma | formation | darrived   | deval      | section         | comment | side_account       | role    | version |
|-----------|:--------:|:---------:|:----------------:|:-------:|:-------:|:-------:|:------:|:-------:|:------:|:------:|:-------:|:----------:|:-------:|:--------:|:------:|:-------:|:---------:|:----------:|:----------:|:---------------:|:-------:|:------------------:|:-------:|:-------:|
| string    | string   | string    | encrypted string | integer | string  | A or D  | string | string  | string | string | string  | yyyy-mm-dd | string  | string   | string | string  | string    | yyyy-mm-dd | yyyy-mm-dd | 0 or id_section | string  | 0 or id_prescriber | string  | v2      |


## Analysis repository
| version | id_ana | id_owner | ana_code | ana_name | ana_abbr | ana_family | ana_unit_rating | ana_value_rating | ana_comment | ana_bio_product | ana_sample_type | ana_type  | ana_active | ana_whonet | id_link | link_ana_ref | link_var_ref | link_pos | link_num_var | link_oblig | id_var | var_label | var_descr | var_unit | var_min | var_max | var_comment | var_res_type | var_formula | var_accu | var_code | var_whonet | var_qrcode | var_highlight |
|--------|:--------:|:--------:|:--------:|:--------:|:----------:|:---------------:|:----------------:|:-----------:|:---------------:|:---------------:|:-----------:|:----------:|:----------:|:-------:|:------------:|:------------:|:--------:|:------------:|:----------:|:------:|:---------:|:---------:|:--------:|:-------:|:-------:|:-----------:|:-----------------:|:-----------:|:--------:|:--------:|:----------:|:-------:|:-------:|
| v3 | id_ana | integer  | string   | string   | string   | id_family  | string          | float            | string      | id_product      | id_sample_type  | id_ana_type | Y or N     | Y or N     | id_link  | id_ana      | id_var       | integer  | integer      | Y or N     | id_var | string    | string    | id_unit  | float   | float   | string      | id_res_type  | string      | integer  | string   | Y or N     | Y or N     | Y or N     |

## Dictionnary
| version | id_data | id_owner | dico_name  | label       | short_label | position | code       | dico_descr | dict_formatting |
|---------|:-------:|:--------:|:----------:|:-----------:|:-----------:|:--------:|:----------:|:----------:|:---------------:|
| v1      | serial  | integer  | string(20) | string(255) | string(20)  | integer  | string(10) | text       | Y or N          |

## Zip code and city
| zip_code | city_name |
|----------|:---------:|
| string   | string    |


> Note :
>
> - First row as column heading
> - Keep the columns in the same order
> - For analysis import the syntax of columns must be identical
