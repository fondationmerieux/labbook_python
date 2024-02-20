# -*- coding: utf-8 -*-
class Constants:
    cst_content_type_plain = 1
    cst_content_type_json  = 2

    cst_isodate   = '%Y-%m-%d'
    cst_dt_ext_HM = '%Y-%m-%dT%H:%M'
    cst_dt_HMS    = '%Y-%m-%d %H:%M:%S'
    cst_dt_HM     = '%Y-%m-%d %H:%M'
    cst_dt_long   = "%d/%m/%Y à %H:%M"
    cst_date_eu   = '%d/%m/%Y'
    cst_date_us   = '%m/%d/%Y'
    cst_date_ymd  = '%Y%m%d'
    cst_time_HM   = '%H:%M'

    cst_storage     = '/storage'
    cst_io          = '/storage/io/'
    cst_key         = '/storage/key/'
    cst_log         = '/storage/log/'
    cst_report      = '/storage/report/'
    cst_resource    = '/storage/resource/'
    cst_dhis2       = '/storage/resource/dhis2/'
    cst_epidemio    = '/storage/resource/epidemio/'
    cst_indicator   = '/storage/resource/indicator/'
    cst_template    = '/storage/resource/template/'
    cst_upload      = '/storage/upload/'
    cst_path_tmp    = '/home/apps/labbook_BE/labbook_BE/tmp/'
    cst_path_script = '/home/apps/labbook_BE/labbook_BE/script/'
    cst_path_lang   = '/home/apps/labbook_BE/labbook_BE/app/translations/'
    cst_path_log    = '/home/apps/logs/'

    cst_script_user     = 'user_labbook'
    cst_script_backup   = 'backup.sh '
    cst_script_analyzer = 'analyzer.sh '

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

    cst_user_type_api = 'API'

    cst_filedata_report     = 'data_template_report'
    cst_filedata_sticker    = 'data_template_sticker'
    cst_filedata_outsourced = 'data_template_outsourced'

    # HL7 Constants
    cst_stat_init    = 'IN'
    cst_stat_pending = 'PD'
