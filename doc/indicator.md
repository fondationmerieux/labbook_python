The [inidicator.ini](storage/resource/indicator/indicator.ini) file must be present and compliant (UTF-8 encoding)

[SETTINGS] section
version : version number
nb_disease : number of disease defined

If nb_disease = 4 then [DISEASE_1] to [DISEASE_4] need to be defined

[DISEASE_xxx] section
disease : label of disease
sample_type : list of serial corresponding to the type of sample in the database (cf table below) or 0, useful for display not for formula, enenv for one serial you have to write it like this : [my_serial]
nb_res : number of result to display

If nb_res = 4 then res_label_1 to res_label_4, formula_1 to formula_4 and sample_type_1 to sample_type_4  need to be defined

res_label_xxx : label of result to display
formula_xxx : formula will be read and interpreted by LabBook (cf DHIS2.md filter section, same algorithm)

Note : formula with a AND first part use first sample_type and second part use second sample_type, if they use same sample_type you should write sampletype like this : [serial_of_first_sample_type, serial_of_second_sample_type]

If formula_xxx is empty then res_label_xxx will be considered as a separation title and sample_type_xxx will not be necessary

sample_type_xxx : serial corresponding to the type of sample in the database (cf table below) or 0, useful for calculate with the formula_xxx


LIST OF SAMPLING TYPES

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
