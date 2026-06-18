| Name                             | Category     | Use                                        |
|----------------------------------|--------------|--------------------------------------------|
| sigl_01_data                     | REQ SAMPLE   | request for a sample                       |
| sigl_01_deleted                  | REQ SAMPLE   | deleted request for a sample               |
| sigl_02_data                     | RECORD       | record                                     |
| sigl_02_deleted                  | RECORD       | deleted record                             |
| sigl_03_data                     | PATIENT      | patient                                    |
| sigl_04_data                     | REQ ANALYSIS | request for analysis                       |
| sigl_04_deleted                  | REQ ANALYSIS | deleted request for analysis               |
| sigl_05_07_data                  | LINK ANA-VAR | link analysis with variable                |
| sigl_05_07_data_test             | LINK ANA-VAR | link analysis with variable (test)         |
| sigl_05_data                     | REF ANALYSIS | analysis details                           |
| sigl_05_data_test                | REF ANALYSIS | analysis details (test)                    |
| sigl_06_data                     | DEFAULT VAL  | default values in preferences              |
| sigl_07_data                     | REF VARIABLE | variable definition                        |
| sigl_07_data_test                | REF VARIABLE | variable definition (test)                 |
| sigl_08_data                     | DOCTOR       | doctor                                     |
| sigl_09_data                     | RESULT       | analysis result                            |
| sigl_09_deleted                  | RESULT       | deleted analysis result                    |
| sigl_10_data                     | VALIDATION   | validation of result                       |
| sigl_10_deleted                  | VALIDATION   | deleted validation                         |
| sigl_11_data                     | FILE         | report file                                |
| sigl_11_deleted                  | FILE         | deleted report file                        |
| sigl_14_data                     | DHIS2        | surveillance epidemio and dhis2            |
| sigl_15_data                     | DHIS2        | epidemiological surveillance details       |
| sigl_dico_data                   | DICTIONARY   | dictionary                                 |
| sigl_equipement_data             | EQUIPMENT    | equipment details                          |
| sigl_evtlog_data                 | LOG          | event log                                  |
| sigl_file_data                   | FILE         | file metadata (path, hash...)              |
| sigl_fournisseurs_data           | SUPPLIER     | supplier                                   |
| sigl_manuels_data                | MANUAL       | manual                                     |
| sigl_non_conformite_data         | CONFORMITY   | non conformity                             |
| sigl_param_cr_data               | SETTINGS     | report parameters                          |
| sigl_pj_role                     | USER         | user role                                  |
| sigl_pj_sequence                 | -            | last sequence numbers                      |
| sigl_procedures_data             | PROCEDURE    | procedure                                  |
| sigl_reunion_data                | MEETING      | meeting                                    |
| sigl_storage_data                | FILE         | file storage paths                         |
| sigl_user_data                   | USER         | users                                      |
| age_interval_setting             | SETTINGS     | age ranges parameter                       |
| alembic_version                  | -            | alembic migration version                  |
| analyzer_msg                     | ANALYZER     | hl7 message exchange with analyzer         |
| analyzer_result                  | ANALYZER     | result from analyzer                       |
| analyzer_setting                 | SETTINGS     | analyzer connection settings               |
| backup_setting                   | SETTINGS     | backup parameters                          |
| connect_setting                  | SETTINGS     | settings for Connect                       |
| control_external                 | QUALITY      | external quality control values            |
| control_internal                 | QUALITY      | internal quality control values            |
| control_quality                  | QUALITY      | list of controls (internal/external)       |
| ctrl_ext_res_report_file         | FILE         | attached report file                       |
| database_status                  | LOG          | status of last referential import          |
| dhis2_setting                    | SETTINGS     | dhis2 settings                             |
| eqp_calibration_file             | FILE         | calibration file                           |
| eqp_document                     | EQUIPMENT    | link equipment with documents              |
| eqp_failure                      | EQUIPMENT    | equipment failure and repair               |
| eqp_failure_file                 | FILE         | failure file                               |
| eqp_invoice_file                 | FILE         | invoice file                               |
| eqp_maintenance_contract         | EQUIPMENT    | equipment maintenance contract             |
| eqp_maintenance_file             | FILE         | maintenance file                           |
| eqp_metrology                    | EQUIPMENT    | metrology and calibration                  |
| eqp_photo_file                   | FILE         | equipment photo                            |
| eqp_preventive_maintenance       | EQUIPMENT    | preventive maintenance                     |
| eqp_preventive_maintenance_file  | FILE         | preventive maintenance file                |
| form_setting                     | SETTINGS     | structure of form fields                   |
| functionnal_unit                 | SETTINGS     | functional unit                            |
| functionnal_unit_link            | SETTINGS     | link functional units                      |
| init_version                     | LOG          | init marker after alembic                  |
| internal_messaging               | MESSAGE      | internal messaging                         |
| internal_messaging_file          | FILE         | file linked to internal message            |
| lab_chart_file                   | FILE         | chart file                                 |
| lite_setting                     | SETTINGS     | Lite configuration settings                |
| lite_users                       | SETTINGS     | associate user with Lite config            |
| manual_file                      | FILE         | manual file                                |
| manual_setting                   | SETTINGS     | manual settings                            |
| meeting_file                     | FILE         | meeting file                               |
| nationality                      | DICTIONARY   | list of nationalities                      |
| patient_form_item                | PATIENT      | dynamic patient data fields                |
| printer_setting                  | SETTINGS     | printer linked to script                   |
| procedure_file                   | FILE         | procedure file                             |
| product_details                  | STOCK        | product sheet                              |
| product_local                    | SETTINGS     | localization of stock product              |
| product_supply                   | STOCK        | product supply                             |
| product_use                      | STOCK        | product usage                              |
| profile_permissions              | USER         | permissions linked to rights               |
| profile_rights                   | USER         | list of rights                             |
| profile_role                     | USER         | user role definition                       |
| record_file                      | FILE         | attached file                              |
| record_file_deleted              | FILE         | deleted attached file                      |
| record_setting                   | SETTINGS     | record number parameters                   |
| record_validation                | RECORD       | comment on biological validation           |
| requesting_services              | SETTINGS     | list of requesting services                |
| sample_destock                   | ALIQUOT      | destocked aliquot                          |
| sending_event                    | SENDING      | sending event log                          |
| sending_method                   | SENDING      | sending method (generic)                   |
| sending_method_mailjet           | SENDING      | mailjet sending method                     |
| sending_method_smtp              | SENDING      | smtp sending method                        |
| sending_method_whatsapp          | SENDING      | whatsapp sending method                    |
| sending_model                    | SENDING      | sending model definition                   |
| stock_setting                    | SETTINGS     | stock settings                             |
| storage_aliquot                  | ALIQUOT      | aliquot                                    |
| storage_box                      | ALIQUOT      | storage box                                |
| storage_chamber                  | ALIQUOT      | storage chamber                            |
| storage_compartment              | ALIQUOT      | storage compartment                        |
| storage_room                     | ALIQUOT      | storage room                               |
| template_setting                 | SETTINGS     | document template settings                 |
| trace_download                   | QUALITY      | trace of downloaded files                  |
| translations                     | LANGUAGE     | translations for search fields             |
| user_cv_file                     | FILE         | user CV file                               |
| user_diploma_file                | FILE         | user diploma file                          |
| user_evaluation_file             | FILE         | user evaluation file                       |
| user_permissions                 | USER         | custom user permissions                    |
| user_signature_file              | FILE         | user signature file                        |
| user_training_file               | FILE         | user training file                         |
| zip_city                         | DICTIONARY   | list of zip codes and cities               |
| automation_job                   | AUTOMATION   | scheduled task definition                  |
| automation_run                   | AUTOMATION   | scheduled task execution history           |
| oauth2_client                    | AUTH         | oauth2 client registration                 |
| oauth2_code                      | AUTH         | oauth2 authorization codes                 |
| oauth2_token                     | AUTH         | oauth2 access and refresh tokens           |
| patient_hist_form_item           | PATIENT      | historical patient dynamic fields          |
| audit_trail                      | AUDIT        | audit trail                                |

119 tables used

