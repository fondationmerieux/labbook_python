# -*- coding: utf-8 -*-
class Constants:
    cst_content_type_plain = "text/plain"
    cst_content_type_csv   = "text/csv"
    cst_content_type_json  = "application/json"
    cst_content_type_hl7   = "application/hl7-v2"
    cst_content_type_pdf   = "application/pdf"

    cst_isodate    = '%Y-%m-%d'
    cst_dt_ext_HM  = '%Y-%m-%dT%H:%M'
    cst_dt_HMS     = '%Y-%m-%d %H:%M:%S'
    cst_dt_HMS_SQL = '%Y-%m-%d %H:%i:%S'
    cst_dt_HM      = '%Y-%m-%d %H:%M'
    cst_dt_HM_SQL  = '%Y-%m-%d %H:%i'
    cst_dt_long    = "%d/%m/%Y à %H:%M"
    cst_date_eu    = '%d/%m/%Y'
    cst_date_us    = '%m/%d/%Y'
    cst_date_ymd   = '%Y%m%d'
    cst_time_HM    = '%H:%M'

    cst_storage     = '/storage'
    cst_io          = '/storage/io/'
    cst_key         = '/storage/key/'
    cst_log         = '/storage/log/'
    cst_resource    = '/storage/resource/'
    cst_audit       = '/storage/resource/audit/'
    cst_dhis2       = '/storage/resource/dhis2/'
    cst_epidemio    = '/storage/resource/epidemio/'
    cst_indicator   = '/storage/resource/indicator/'
    cst_template    = '/storage/resource/template/'
    cst_photo       = '/storage/resource/photo/'
    cst_printer     = '/storage/resource/printer/'
    cst_report      = '/storage/report/'
    cst_upload      = '/storage/upload/'

    cst_dhis2_upload    = '/storage/upload/dhis2/'
    cst_activity_upload = '/storage/upload/activity/'
    cst_billing_upload  = '/storage/upload/billing/'

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
    cst_filedata_invoice    = 'data_template_invoice'
    cst_filedata_billing_status = 'data_template_billing_status'
    cst_filedata_activity_report = 'data_template_activity_report'

    # Type or validation
    cst_tech_vld = 251
    cst_bio_vld = 252

    # HL7 Constants
    cst_stat_init      = 'IN'
    cst_stat_pending   = 'PD'
    cst_stat_wrong_cnx = 'WC'
    cst_stat_accepted  = 'AA'
    cst_stat_error     = 'AE'
    cst_stat_rejected  = 'AR'

    cst_email_test = "test-labbook@yopmail.com"

    cst_base_whatsapp  = "https://graph.facebook.com/v23.0"
    cst_msg_whatsapp   = cst_base_whatsapp + "/{pnid}/messages"
    cst_media_whatsapp = cst_base_whatsapp + "/{pnid}/media"
    cst_model_test_whatsapp = "hello_world"

    # example : report_2025-10-06.pdf
    cst_safe_pattern = r'[^A-Za-z0-9._-]+'
    # example : name="Alice" → ('name','"', 'Alice')
    cst_keyvalue_pattern = r'(\w+)\s*=\s*([\'"])(.*?)\2'
