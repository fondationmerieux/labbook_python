# -*- coding: utf-8 -*-
class Constants:
    cst_content_type_plain = 1
    cst_content_type_json  = 2

    cst_isodate  = '%Y-%m-%d'
    cst_isodatetime = '%Y-%m-%d %H:%M:%S'
    cst_date_eu  = '%d/%m/%Y'
    cst_date_us  = '%m/%d/%Y'
    cst_date_ymd = '%Y%m%d'

    cst_storage  = '/storage'
    cst_io       = '/storage/io/'
    cst_key      = '/storage/key/'
    cst_log      = '/storage/log/'
    cst_report   = '/storage/report/'
    cst_resource = '/storage/resource/'
    cst_dhis2    = '/storage/resource/dhis2/'
    cst_epidemio = '/storage/resource/epidemio/'
    cst_template = '/storage/resource/template/'
    cst_upload   = '/storage/upload/'

    cst_path_tmp    = '/home/apps/labbook_BE/labbook_BE/tmp/'
    cst_path_script = '/home/apps/labbook_BE/labbook_BE/script/'
    cst_path_lang   = '/home/apps/labbook_BE/labbook_BE/app/translations/'

    cst_script_user   = 'user_labbook'
    cst_script_backup = 'backup.sh '

    # CMD LIST for backup & restore
    cst_io_backup      = 'backup'
    cst_io_genkey      = 'genkey'
    cst_io_initmedia   = 'initmedia'
    cst_io_keyexist    = 'keyexist'
    cst_io_listmedia   = 'listmedia'
    cst_io_listarchive = 'listarchive'
    cst_io_progbackup  = 'progbackup'
    cst_io_restart     = 'restart'
    cst_io_restore     = 'restore'

    cst_user_active   = 'A'
    cst_user_inactive = 'D'
    cst_user_deleted  = 'X'
