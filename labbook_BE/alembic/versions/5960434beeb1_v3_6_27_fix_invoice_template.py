# -*- coding:utf-8 -*-
"""v3_6_27_fix_invoice_template

Revision ID: 5960434beeb1
Revises: b54ea0468f8a
Create Date: 2026-10-07 15:00:00.000000

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = '5960434beeb1'
down_revision = 'b54ea0468f8a'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_27_fix_invoice_template revision=5960434beeb1")

    # Overwrite the default invoice template: discount lines were never displayed
    try:
        import os
        import shutil

        os.makedirs("/storage/resource/template", exist_ok=True)
        shutil.copy2("alembic/resource/template/tpl_invoice.odt", "/storage/resource/template/tpl_invoice.odt")
    except Exception as err:
        print("ERROR copy tpl_invoice.odt,\n\terr=" + str(err))

    # Get the current
    conn = op.get_bind()

    # Insert profile rights for the register
    try:
        conn.execute(text('''
                          insert into profile_rights (prr_ser, prr_date, prr_by_user, prr_rank, prr_type, prr_label, prr_tag)
                          values
                          (184, NOW(), 0, 4000,"REGISTER","Consulter le registre", "REGISTER_184"),
                          (185, NOW(), 0, 4020,"REGISTER","Télécharger le registre", "REGISTER_185")
                          '''))
    except Exception as err:
        print("ERROR insert new default profile_rights,\n\terr=" + str(err))

    # Default permissions of the register: biologist, technician, advanced technician, quality technician, quality officer
    try:
        conn.execute(text('''
                          INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
                          SELECT NOW(), 0, pro.pro_ser, prr.prr_ser, if(pro.pro_role in (2, 3, 5, 6, 8), 'Y', 'N')
                          FROM profile_role AS pro
                          JOIN profile_rights AS prr ON prr.prr_ser BETWEEN 184 AND 185
                        '''))
    except Exception as err:
        print("ERROR inserting new default profile_permissions for register,\n\terr=" + str(err))

    # Rename legacy sigl_ tables to the new naming convention
    try:
        conn.execute(text('rename table sigl_evtlog_data to event_log'))
        conn.execute(text('''
                          alter table event_log
                          change column id_data evl_ser int unsigned NOT NULL AUTO_INCREMENT,
                          change column id_owner evl_user int unsigned DEFAULT NULL,
                          change column evt_datetime evl_date datetime DEFAULT NULL,
                          change column evt_type evl_type int unsigned DEFAULT NULL,
                          change column evt_name evl_name varchar(255) DEFAULT NULL,
                          change column message evl_message varchar(255) DEFAULT NULL,
                          rename index id_owner to evl_user
                          '''))
    except Exception as err:
        print("ERROR rename sigl_evtlog_data to event_log,\n\terr=" + str(err))

    try:
        conn.execute(text('rename table sigl_param_cr_data to report_setting'))
        conn.execute(text('''
                          alter table report_setting
                          change column id_data rps_ser int unsigned NOT NULL AUTO_INCREMENT,
                          change column id_owner rps_user int unsigned DEFAULT NULL,
                          change column sys_creation_date rps_date datetime DEFAULT NULL,
                          change column sys_last_mod_date rps_date_upd datetime DEFAULT NULL,
                          change column sys_last_mod_user rps_user_upd int unsigned DEFAULT NULL,
                          change column entete rps_header int unsigned DEFAULT NULL,
                          change column commentaire rps_comment int unsigned DEFAULT NULL,
                          change column report_pwd rps_pwd varchar(1) NOT NULL DEFAULT 'N'
                          '''))
    except Exception as err:
        print("ERROR rename sigl_param_cr_data to report_setting,\n\terr=" + str(err))

    try:
        conn.execute(text('rename table sigl_storage_data to file_storage'))
        conn.execute(text('''
                          alter table file_storage
                          change column id_data fst_ser int unsigned NOT NULL AUTO_INCREMENT,
                          change column id_owner fst_user int unsigned DEFAULT NULL,
                          change column sys_creation_date fst_date datetime DEFAULT NULL,
                          change column sys_last_mod_date fst_date_upd datetime DEFAULT NULL,
                          change column sys_last_mod_user fst_user_upd int unsigned DEFAULT NULL,
                          change column path fst_path varchar(255) DEFAULT NULL
                          '''))
    except Exception as err:
        print("ERROR rename sigl_storage_data to file_storage,\n\terr=" + str(err))

    try:
        conn.execute(text('rename table sigl_reunion_data to meeting'))
        conn.execute(text('''
                          alter table meeting
                          change column id_data mee_ser int unsigned NOT NULL AUTO_INCREMENT,
                          change column id_owner mee_user int unsigned DEFAULT NULL,
                          change column sys_creation_date mee_date datetime DEFAULT NULL,
                          change column sys_last_mod_date mee_date_upd datetime DEFAULT NULL,
                          change column sys_last_mod_user mee_user_upd int unsigned DEFAULT NULL,
                          change column date mee_date_meeting date DEFAULT NULL,
                          change column organisateur_id mee_organizer int unsigned DEFAULT NULL,
                          change column type_reu mee_type int unsigned DEFAULT NULL,
                          change column cr mee_report text
                          '''))
    except Exception as err:
        print("ERROR rename sigl_reunion_data to meeting,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_6_27_fix_invoice_template revision=5960434beeb1")


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. To roll back, restore a verified backup
    taken before revision 5960434beeb1.
    """
    print("downgrade skipped: irreversible migration 5960434beeb1 (forward-only policy)")
