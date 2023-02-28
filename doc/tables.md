| Name    	                                 | Category      | Use                                      |
|------------------------------------------------|---------------|------------------------------------------|
| sigl_01_data	                                 | REQ SAMPLE	 | request for a sample                     |
| sigl_01_deleted	                         | REQ SAMPLE    | deleted request for a sample             |
| sigl_01_dico_analyse_data	                 | ?	         | ? update during a merger                 |
| sigl_01_dico_analyse_deleted	                 | ?	         | ? update during a merger                 |
| sigl_02_data	                                 | RECORD	 | record                                   |
| sigl_02_deleted	                         | RECORD	 | record  deleted                          |
| sigl_03_data	                                 | PATIENT	 | patient                                  |
| sigl_04_data	                                 | REQ ANALYSIS	 | request for analysis                     |
| sigl_04_deleted	                         | REQ ANALYSIS	 | deleted request for analysis             |
| sigl_05_07_data	                         | LINK ANA-VAR	 | link between analysis and variable       |
| sigl_05_data	                                 | REF ANALYSIS	 | analysis details                         |
| sigl_06_data	                                 | DEFAULT VAL	 | values in the preferences menu           |
| sigl_07_data	                                 | REF VARIABLE	 | definition variable analysis             |
| sigl_08_data	                                 | DOCTOR	 | doctor                                   |
| sigl_09_data	                                 | RESULT	 | analysis result                          |
| sigl_09_deleted	                         | RESULT	 | analysis result deleted                  |
| sigl_10_data	                                 | VALIDATION	 | validation result analysis               |
| sigl_10_deleted	                         | VALIDATION	 | validation result deleted                |
| sigl_11_data	                                 | FILE	         | report file                              |
| sigl_11_deleted	                         | FILE	         | report file deleted                      |
| sigl_12_data	                                 | ?	         | ? update during a merger                 |
| sigl_12_deleted	                         | ?	         | ? update during a merger                 |
| sigl_14_data	                                 | DHIS2	 | surveillance epidemio and dhis2          |
| sigl_15_data	                                 | DHIS2	 | epidemiological surveillance details     |
| sigl_dico_data	                         | DICTIONNARY	 | dictionnary                              |
| sigl_controle_externe_ctrl_resultat_cr__file_d | FILE          | attached file                            |
| sigl_dos_valisedoc__file_data	                 | FILE	         | attached file                            |
| sigl_dos_valisedoc__file_deleted	         | FILE	         | deleted attachment                       |
| sigl_equipement_certif_etalonnage__file_data	 | FILE	         | attached file                            |
| sigl_equipement_contrat_maintenance__file_data | FILE	         | attached file                            |
| sigl_equipement_data	                         | EQUIPMENT	 | equipment details                        |
| sigl_equipement_facture__file_data	         | FILE	         | attached file                            |
| sigl_equipement_maintenance_preventive__file_d | FILE    	 | attached file                            |
| sigl_equipement_pannes__file_data	         | FILE    	 | attached file                            |
| sigl_equipement_photo__file_data	         | FILE    	 | attached file                            |
| sigl_evtlog_data	                         | LOG	         | log evenement                            |
| sigl_file_data	                         | FILE	         | files details (path, hash...)            |
| sigl_fournisseurs_data	                 | SUPPLIER	 | supplier                                 |
| sigl_laboratoire_organigramme__file_data	 | FILE	         | attached file                            |
| sigl_manuels_data	                         | MANUAL	 | manual                                   |
| sigl_manuels_document__file_data	         | FILE	         | attached file                            |
| sigl_non_conformite_data	                 | CONFORMITY	 | no conformity                            |
| sigl_param_cr_data	                         | SETTINGS	 | report parameter                         |
| sigl_param_num_dos_data	                 | SETTINGS	 | record number parameter                  |
| sigl_pj_role	                                 | USER    	 | user role                                |
| sigl_pj_sequence	                         | -	         | last number (record, bill)               |
| sigl_procedures_data	                         | PROCEDURE	 | procedure                                |
| sigl_procedures_document__file_data     	 | FILE	         | attached file                            |
| sigl_reunion_data	                         | MEETING	 | meeting                                  |
| sigl_reunion_pj__file_data	                 | FILE	         | attached file                            |
| sigl_storage_data	                         | FILE	         | file storage path                        |
| sigl_user_cv__file_data	                 | FILE	         | attached file                            |
| sigl_user_data	                         | USER	         | users                                    |
| sigl_user_diplomes__file_data	                 | FILE	         | attached file                            |
| sigl_user_evaluation__file_data	         | FILE	         | attached file                            |
| sigl_user_formations__file_data	         | FILE	         | attached file                            |
| age_interval_setting	                         | SETTINGS	 | age ranges parameter                     |
| alembic_version	                         | -       	 | version number migration DB by Alembic   |
| backup_setting	                         | SETTINGS	 | backup parameter                         |
| database_status	                         | LOG	         | status of the last referential import    |
| init_version                                   | LOG           | use to start process after alembic once  |
| product_details	                         | STOCK	 | product sheet                            |
| product_supply	                         | STOCK	 | product supply                           |
| product_use	                                 | STOCK	 | product used                             |
| translations  	                         | LANGUAGE	 | translations for search fields           |
| template_setting	                         | SETTINGS	 | setting for template to build document   |
| nationality   	                         | DICTIONNARY	 | list of nationality                      |
| zip_city      	                         | DICTIONNARY	 | list of zip code and city                |
| control_quality      	                         | QUALITY	 | list of control internal and external    |
| control_internal   	                         | QUALITY	 | list of internal control value           |
| control_external     	                         | QUALITY	 | list of external control value           |
| requesting_services                            | SETTINGS      | list of requesting services              |
| functionnal_unit                               | SETTINGS      | list of functionnal units                |
| functionnal_unit_link                          | SETTINGS      | list of links for functionnal units      |
| stock_setting                                  | SETTINGS      | settings for stock                       |
| list_comment                                   | COMMENT       | structure for keep history of comments   |
| form_setting                                   | SETTINGS      | structure for enable or disabled fields  |

77 tables used


| Name    	                                 |
| sigl_03_deleted                                |                                
| sigl_05_05_data                                |
| sigl_05_deleted                                |
| sigl_07_deleted                                |
| sigl_08_deleted                                |
| sigl_13_data                                   |
| sigl_16_data                                   |
| sigl_dico_deleted                              |
| sigl_equipement_deleted                        |
| sigl_fournisseurs_deleted                      |
| sigl_laboratoire_data                          |

11 tables unused but not deleted yet
