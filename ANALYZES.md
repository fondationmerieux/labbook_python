List of analyzes added during the database migration process

Example of possible conflict:
If you restore a backup from a V2.5 with a modified repository where the lab added a B650 analysis, after the restore a database migration process start.
Like we see in list below a B650 analysis is added, analysis code are unique, this addition will be a failure.

ADDED ANALYZES
- added from 2.9.1 : B650, B651, B652, B653, B654, B655, B656, B657, B658, B670, B671, B672, B673, B674, B675, B676, B677, B678
- added from 3.0.3 : B5271a, B5271b, B4274, B4719, B4721
- added from 3.0.5 : E01, E02, E03, E04, E05
- added from 3.0.7 : B659, B660, B661, B679, B680, B681
- added from 3.0.8 : B796, B797,  B798, B799, B800, B801, E06
- added from 3.0.9 : PB25

DELETED ANALYZES
- deleted from 3.0.2 : B603
- deleted from 3.0.4 : B171
