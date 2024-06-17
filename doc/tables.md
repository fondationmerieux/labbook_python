| Name    	                                 | Category      | Use                                      |
|------------------------------------------------|---------------|------------------------------------------|
| sigl\_01\_data	                         | REQ SAMPLE	 | request for a sample                     |
| sigl\_01\_deleted	                         | REQ SAMPLE    | deleted request for a sample             |
| sigl\_02\_data	                         | RECORD	 | record                                   |
| sigl\_02\_deleted	                         | RECORD	 | record  deleted                          |
| sigl\_03\_data	                         | PATIENT	 | patient                                  |
| sigl\_04\_data	                         | REQ ANALYSIS	 | request for analysis                     |
| sigl\_04\_deleted	                         | REQ ANALYSIS	 | deleted request for analysis             |
| sigl\_05\_07\_data	                         | LINK ANA-VAR	 | link between analysis and variable       |
| sigl\_05\_07\_data\_test	                 | LINK ANA-VAR	 | link between analysis and variable test  |
| sigl\_05\_data	                         | REF ANALYSIS	 | analysis details                         |
| sigl\_05\_data\_test                           | REF ANALYSIS	 | analysis details for testing             |
| sigl\_06\_data	                         | DEFAULT VAL	 | values in the preferences menu           |
| sigl\_07\_data	                         | REF VARIABLE	 | definition variable analysis             |
| sigl\_07\_data\_test                           | REF VARIABLE	 | definition variable analysis for testing |
| sigl\_08\_data	                         | DOCTOR	 | doctor                                   |
| sigl\_09\_data	                         | RESULT	 | analysis result                          |
| sigl\_09\_deleted	                         | RESULT	 | analysis result deleted                  |
| sigl\_10\_data	                         | VALIDATION	 | validation result analysis               |
| sigl\_10\_deleted	                         | VALIDATION	 | validation result deleted                |
| sigl\_11\_data	                         | FILE	         | report file                              |
| sigl\_11\_deleted	                         | FILE	         | report file deleted                      |
| sigl\_14\_data	                         | DHIS2	 | surveillance epidemio and dhis2          |
| sigl\_15\_data	                         | DHIS2	 | epidemiological surveillance details     |
| sigl\_dico\_data	                         | DICTIONNARY	 | dictionnary                              |
| ctrl\_ext\_res\_report\_file                   | FILE          | attached file                            |
| record\_file           	                 | FILE	         | attached file                            |
| record\_file\_deleted           	         | FILE	         | deleted attachment                       |
| record\_validation           	                 | RECORD        | save comment of biological validation    |
| eqp\_calibration\_file                  	 | FILE	         | attached file                            |
| eqp\_maintenance\_file                         | FILE	         | attached file                            |
| sigl\_equipement\_data	                 | EQUIPMENT	 | equipment details                        |
| eqp\_invoice\_file                  	         | FILE	         | attached file                            |
| eqp\_preventive\_maintenance\_file             | FILE    	 | attached file                            |
| eqp\_failure\_file              	         | FILE    	 | attached file                            |
| eqp\_photo\_file                 	         | FILE    	 | attached file                            |
| sigl\_evtlog\_data	                         | LOG	         | log evenement                            |
| sigl\_file\_data	                         | FILE	         | files details (path, hash...)            |
| sigl\_fournisseurs\_data	                 | SUPPLIER	 | supplier                                 |
| lab\_chart\_file                        	 | FILE	         | attached file                            |
| sigl\_manuels\_data	                         | MANUAL	 | manual                                   |
| manual\_file                   	         | FILE	         | attached file                            |
| sigl\_non\_conformite\_data	                 | CONFORMITY	 | no conformity                            |
| sigl\_param\_cr\_data	                         | SETTINGS	 | report parameter                         |
| sigl\_param\_num\_dos\_data	                 | SETTINGS	 | record number parameter                  |
| sigl\_pj\_role	                         | USER    	 | user role                                |
| sigl\_pj\_sequence	                         | -	         | last number (record, bill)               |
| sigl\_procedures\_data	                 | PROCEDURE	 | procedure                                |
| procedure\_file                             	 | FILE	         | attached file                            |
| sigl\_reunion\_data	                         | MEETING	 | meeting                                  |
| meeting\_file          	                 | FILE	         | attached file                            |
| sigl\_storage\_data	                         | FILE	         | file storage path                        |
| user\_cv\_file          	                 | FILE	         | attached file                            |
| sigl\_user\_data	                         | USER	         | users                                    |
| user\_diploma\_file     	                 | FILE	         | attached file                            |
| user\_evaluation\_file          	         | FILE	         | attached file                            |
| user\_training\_file            	         | FILE	         | attached file                            |
| age\_interval\_setting	                 | SETTINGS	 | age ranges parameter                     |
| alembic\_version	                         | -       	 | version number migration DB by Alembic   |
| backup\_setting	                         | SETTINGS	 | backup parameter                         |
| database\_status	                         | LOG	         | status of the last referential import    |
| init\_version                                  | LOG           | use to start process after alembic once  |
| product\_details	                         | STOCK	 | product sheet                            |
| product\_supply	                         | STOCK	 | product supply                           |
| product\_use	                                 | STOCK	 | product used                             |
| product\_local                                 | SETTINGS      | list of localization of stock product    |
| translations  	                         | LANGUAGE	 | translations for search fields           |
| template\_setting	                         | SETTINGS	 | setting for template to build document   |
| nationality   	                         | DICTIONNARY	 | list of nationality                      |
| zip\_city      	                         | DICTIONNARY	 | list of zip code and city                |
| control\_quality      	                 | QUALITY	 | list of control internal and external    |
| control\_internal   	                         | QUALITY	 | list of internal control value           |
| control\_external     	                 | QUALITY	 | list of external control value           |
| requesting\_services                           | SETTINGS      | list of requesting services              |
| functionnal\_unit                              | SETTINGS      | list of functionnal units                |
| functionnal\_unit\_link                        | SETTINGS      | list of links for functionnal units      |
| stock\_setting                                 | SETTINGS      | settings for stock                       |
| ~~list\_comment~~                              | COMMENT       | **will be removed 3.5 version**          |
| form\_setting                                  | SETTINGS      | structure for enable or disabled fields  |
| trace\_download                                | QUALITY       | tracks file downloads (only procedure)   |
| manual\_setting                                | SETTINGS      | settings for manual                      |
| eqp\_document                                  | EQUIPMENT     | link equipment with documents            |
| eqp\_preventive\_maintenance                   | EQUIPMENT     | link equipment with preventive mainten.  |
| eqp\_maintenance\_contract                     | EQUIPMENT     | link equipment with maintenance contract |
| eqp\_failure                                   | EQUIPMENT     | link equipment with failure and repair   |
| eqp\_metrology                                 | EQUIPMENT     | link equipment with metrology and calib. |
| patient\_form\_item                            | PATIENT	 | patient data for dynamical fields        |
| analyzer\_lab28                                | ANALYZER	 | hl7 message to and from analyzer         |
| analyzer\_setting                              | SETTINGS	 | settings for analyzer connection         |
| lab\_chart\_file                               | FILE  	 | chart file of laboratory                 |

87 tables used
