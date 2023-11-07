| Name    	                                 | Category      | Use                                      |
|------------------------------------------------|---------------|------------------------------------------|
| sigl_01_data	                                 | REQ SAMPLE	 | request for a sample                     |
| sigl_01_deleted	                         | REQ SAMPLE    | deleted request for a sample             |
| sigl_02_data	                                 | RECORD	 | record                                   |
| sigl_02_deleted	                         | RECORD	 | record  deleted                          |
| sigl_03_data	                                 | PATIENT	 | patient                                  |
| sigl_04_data	                                 | REQ ANALYSIS	 | request for analysis                     |
| sigl_04_deleted	                         | REQ ANALYSIS	 | deleted request for analysis             |
| sigl_05_07_data	                         | LINK ANA-VAR	 | link between analysis and variable       |
| sigl_05_07_data_test	                         | LINK ANA-VAR	 | link between analysis and variable test  |
| sigl_05_data	                                 | REF ANALYSIS	 | analysis details                         |
| sigl_05_data_test                              | REF ANALYSIS	 | analysis details for testing             |
| sigl_06_data	                                 | DEFAULT VAL	 | values in the preferences menu           |
| sigl_07_data	                                 | REF VARIABLE	 | definition variable analysis             |
| sigl_07_data_test                              | REF VARIABLE	 | definition variable analysis for testing |
| sigl_08_data	                                 | DOCTOR	 | doctor                                   |
| sigl_09_data	                                 | RESULT	 | analysis result                          |
| sigl_09_deleted	                         | RESULT	 | analysis result deleted                  |
| sigl_10_data	                                 | VALIDATION	 | validation result analysis               |
| sigl_10_deleted	                         | VALIDATION	 | validation result deleted                |
| sigl_11_data	                                 | FILE	         | report file                              |
| sigl_11_deleted	                         | FILE	         | report file deleted                      |
| sigl_14_data	                                 | DHIS2	 | surveillance epidemio and dhis2          |
| sigl_15_data	                                 | DHIS2	 | epidemiological surveillance details     |
| sigl_dico_data	                         | DICTIONNARY	 | dictionnary                              |
| ctrl_ext_res_report_file                       | FILE          | attached file                            |
| record_file           	                 | FILE	         | attached file                            |
| record_file_deleted           	         | FILE	         | deleted attachment                       |
| eqp_calibration_file                  	 | FILE	         | attached file                            |
| eqp_maintenance_file                           | FILE	         | attached file                            |
| sigl_equipement_data	                         | EQUIPMENT	 | equipment details                        |
| eqp_invoice_file                  	         | FILE	         | attached file                            |
| eqp_preventive_maintenance_file                | FILE    	 | attached file                            |
| eqp_failure_file              	         | FILE    	 | attached file                            |
| eqp_photo_file                 	         | FILE    	 | attached file                            |
| sigl_evtlog_data	                         | LOG	         | log evenement                            |
| sigl_file_data	                         | FILE	         | files details (path, hash...)            |
| sigl_fournisseurs_data	                 | SUPPLIER	 | supplier                                 |
| lab_chart_file                        	 | FILE	         | attached file                            |
| sigl_manuels_data	                         | MANUAL	 | manual                                   |
| manual_file                   	         | FILE	         | attached file                            |
| sigl_non_conformite_data	                 | CONFORMITY	 | no conformity                            |
| sigl_param_cr_data	                         | SETTINGS	 | report parameter                         |
| sigl_param_num_dos_data	                 | SETTINGS	 | record number parameter                  |
| sigl_pj_role	                                 | USER    	 | user role                                |
| sigl_pj_sequence	                         | -	         | last number (record, bill)               |
| sigl_procedures_data	                         | PROCEDURE	 | procedure                                |
| procedure_file                             	 | FILE	         | attached file                            |
| sigl_reunion_data	                         | MEETING	 | meeting                                  |
| meeting_file          	                 | FILE	         | attached file                            |
| sigl_storage_data	                         | FILE	         | file storage path                        |
| user_cv_file          	                 | FILE	         | attached file                            |
| sigl_user_data	                         | USER	         | users                                    |
| user_diploma_file     	                 | FILE	         | attached file                            |
| user_evaluation_file          	         | FILE	         | attached file                            |
| user_training_file            	         | FILE	         | attached file                            |
| age_interval_setting	                         | SETTINGS	 | age ranges parameter                     |
| alembic_version	                         | -       	 | version number migration DB by Alembic   |
| backup_setting	                         | SETTINGS	 | backup parameter                         |
| database_status	                         | LOG	         | status of the last referential import    |
| init_version                                   | LOG           | use to start process after alembic once  |
| product_details	                         | STOCK	 | product sheet                            |
| product_supply	                         | STOCK	 | product supply                           |
| product_use	                                 | STOCK	 | product used                             |
| product_local                                  | SETTINGS      | list of localization of stock product    |
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
| trace_download                                 | QUALITY       | tracks file downloads (only procedure)   |
| manual_setting                                 | SETTINGS      | settings for manual                      |

79 tables used
