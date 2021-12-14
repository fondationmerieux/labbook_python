| Name    	                                 | Category      | Use                                      |
|------------------------------------------------|---------------|------------------------------------------|
| sigl_01_data	                                 | REQ SAMPLE	 | demande de prélèvement                   |
| sigl_01_deleted	                         | REQ SAMPLE    | demande de prélèvement supprimée         |
| sigl_01_dico_analyse_data	                 | ?	         | ? mise a jour lors d'une fusion          |
| sigl_01_dico_analyse_deleted	                 | ?	         | ? mise a jour lors d'une fusion          |
| sigl_02_data	                                 | RECORD	 | dossier                                  |
| sigl_02_deleted	                         | RECORD	 | dossier supprimé                         |
| sigl_03_data	                                 | PATIENT	 | patient                                  |
| sigl_04_data	                                 | REQ ANALYSIS	 | demande d'analyse                        |
| sigl_04_deleted	                         | REQ ANALYSIS	 | demande d'analyse supprimée              |
| sigl_05_07_data	                         | LINK ANA-VAR	 | lien entre analyse et variable           |
| sigl_05_data	                                 | REF ANALYSIS	 | définition analyse                       |
| sigl_06_data	                                 | DEFAULT VAL	 | valeurs du menu préférences              |
| sigl_07_data	                                 | REF VARIABLE	 | définition variable analyse              |
| sigl_08_data	                                 | DOCTOR	 | praticien                                |
| sigl_09_data	                                 | RESULT	 | résultat analyse                         |
| sigl_09_deleted	                         | RESULT	 | résultat analyse supprimé                |
| sigl_10_data	                                 | VALIDATION	 | validation résultat analyse              |
| sigl_10_deleted	                         | VALIDATION	 | validation résultat supprimée            |
| sigl_11_data	                                 | FILE	         | fichier compte-rendu                     |
| sigl_11_deleted	                         | FILE	         | fichier compte-rendu supprimé            |
| sigl_12_data	                                 | ?	         | ? mise a jour lors d'une fusion          |
| sigl_12_deleted	                         | ?	         | ? mise a jour lors d'une fusion          |
| sigl_14_data	                                 | DHIS2	 | surveillance epidemio et dhis2           |
| sigl_15_data	                                 | DHIS2	 | details sruveillance epidemio            |
| sigl_dico_data	                         | DICTIONNARY	 | dictionnaire                             |
| sigl_dos_valisedoc__file_data	                 | FILE	         | fichier piece jointe                     |
| sigl_dos_valisedoc__file_deleted	         | FILE	         | fichier piece jointe supprimé            |
| sigl_equipement_certif_etalonnage__file_data	 | FILE	         | fichier piece jointe                     |
| sigl_equipement_contrat_maintenance__file_data | FILE	         | fichier piece jointe                     |
| sigl_equipement_data	                         | EQUIPMENT	 | equipement                               |
| sigl_equipement_facture__file_data	         | FILE	         | fichier piece jointe                     |
| sigl_equipement_maintenance_preventive__file_d | FILE    	 | fichier piece jointe                     |
| sigl_equipement_pannes__file_data	         | FILE    	 | fichier piece jointe                     |
| sigl_equipement_photo__file_data	         | FILE    	 | fichier piece jointe                     |
| sigl_evtlog_data	                         | LOG	         | log evenement                            |
| sigl_file_data	                         | FILE	         | info fichier (chemin, hash...)           |
| sigl_fournisseurs_data	                 | SUPPLIER	 | fournisseur                              |
| sigl_laboratoire_organigramme__file_data	 | FILE	         | fichier piece jointe                     |
| sigl_manuels_data	                         | MANUAL	 | manuel                                   |
| sigl_manuels_document__file_data	         | FILE	         | fichier piece jointe                     |
| sigl_non_conformite_data	                 | CONFORMITY	 | non conformité                           |
| sigl_param_cr_data	                         | SETTINGS	 | paramètre compte-rendu                   |
| sigl_param_num_dos_data	                 | SETTINGS	 | paramètre numéro de dossier              |
| sigl_pj_group	                                 | USER	         | login and id_group                       |
| sigl_pj_group_link	                         | USER	         | id_group, id_group_parent et id_role     |
| sigl_pj_role	                                 | USER    	 | role utilisateur                         |
| sigl_pj_sequence	                         | -	         | dernier numéro (dossier, facture)        |
| sigl_procedures_data	                         | PROCEDURE	 | procédure                                |
| sigl_procedures_document__file_data     	 | FILE	         | fichier piece jointe                     |
| sigl_reunion_data	                         | MEETING	 | réunion                                  |
| sigl_reunion_pj__file_data	                 | FILE	         | fichier piece jointe                     |
| sigl_storage_data	                         | FILE	         | chemin de stockage fichier               |
| sigl_user_cv__file_data	                 | FILE	         | fichier piece jointe                     |
| sigl_user_data	                         | USER	         | utilisateur                              |
| sigl_user_diplomes__file_data	                 | FILE	         | fichier piece jointe                     |
| sigl_user_evaluation__file_data	         | FILE	         | fichier piece jointe                     |
| sigl_user_formations__file_data	         | FILE	         | fichier piece jointe                     |
| age_interval_setting	                         | SETTINGS	 | paramètre interval age                   |
| alembic_version	                         | -       	 | numéro de version migration alembic      |
| backup_setting	                         | SETTINGS	 | paramètre sauvegarde                     |
| database_status	                         | LOG	         | statut du dernier import référentiel     |
| init_version                                   | LOG           | use to start process after alembic once  |
| product_details	                         | STOCK	 | fiche produit                            |
| product_supply	                         | STOCK	 | approvisionnement produit                |
| product_use	                                 | STOCK	 | product used                             |
| translations  	                         | LANGUAGE	 | translations for search fields           |
| template_setting	                         | SETTINGS	 | setting for PDF template                 |
| nationality   	                         | DICTIONNARY	 | list of nationality                      |

68 tables used
