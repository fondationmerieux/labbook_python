# -*- coding:utf-8 -*-
"""v3_4_3_new_ui_equipment

Revision ID: e038e2ab0b42
Revises: 7d7ebdf6d2c6
Create Date: 2024-02-26 14:40:42.189855

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'e038e2ab0b42'
down_revision = '7d7ebdf6d2c6'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_4_3_new_ui_equipment revision=e038e2ab0b42")

    # Get the current
    conn = op.get_bind()

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/photo").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/photo,\n\terr=" + str(err))

    # MOVE photo from eqp_photo_file to resource/photo/
    try:
        import os

        l_files = conn.execute(text("select generated_name, path, content_type from sigl_file_data "
                                    "where id_data in (select id_file from eqp_photo_file)"))

        rows = l_files.fetchall()

        for row in rows:
            if row[2].startswith("image"):
                src_img_path = os.path.join("/storage/upload/" + row[1], row[0])
                dst_img_dir  = "/storage/resource/photo/" + row[1]
                dst_img_path = os.path.join(dst_img_dir, row[0])

                if os.path.exists(src_img_path):
                    if not os.path.exists(dst_img_dir):
                        os.makedirs(dst_img_dir)

                    os.replace(src_img_path, dst_img_path)
                    print("Photo {} moved successfully to {}.\n".format(row[0], dst_img_dir))
            else:
                print("CONFLICT move photo generated_name=" + str(row[0]) + " content_type=" + str(row[2])  + "\n")

    except Exception as err:
        print("ERROR move photo from eqp_photo_file,\n\terr=" + str(err))

    # Create table eqp_document
    try:
        conn.execute(text("create table if not exists eqp_document("
                          "eqd_ser int not NULL AUTO_INCREMENT,"
                          "eqd_date DATETIME,"
                          "eqd_user INT default 0,"
                          "eqd_eqp INT NOT NULL,"
                          "eqd_type varchar(4) NOT NULL,"
                          "eqd_ref INT NOT NULL,"
                          "PRIMARY KEY (eqd_ser),"
                          "INDEX (eqd_eqp), INDEX (eqd_type)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table eqp_document,\n\terr=" + str(err))

    # Create table eqp_failure
    try:
        conn.execute(text("create table if not exists eqp_failure("
                          "eqf_ser int not NULL AUTO_INCREMENT,"
                          "eqf_date DATETIME,"
                          "eqf_user INT default 0,"
                          "eqf_eqp INT NOT NULL,"
                          "eqf_type varchar(4) NOT NULL,"
                          "eqf_incharge INT NOT NULL,"
                          "eqf_supplier INT NOT NULL,"
                          "eqf_comm text not null default '',"
                          "PRIMARY KEY (eqf_ser),"
                          "INDEX (eqf_eqp), INDEX (eqf_type)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table eqp_failure,\n\terr=" + str(err))

    # Create table eqp_metrology
    try:
        conn.execute(text("create table if not exists eqp_metrology("
                          "eqm_ser int not NULL AUTO_INCREMENT,"
                          "eqm_date DATETIME,"
                          "eqm_user INT default 0,"
                          "eqm_eqp INT NOT NULL,"
                          "eqm_supplier INT NOT NULL,"
                          "eqm_comm text not null default '',"
                          "PRIMARY KEY (eqm_ser),"
                          "INDEX (eqm_eqp)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table eqp_metrology,\n\terr=" + str(err))

    # Create table eqp_preventive_maintenance
    try:
        conn.execute(text("create table if not exists eqp_preventive_maintenance("
                          "eqs_ser int not NULL AUTO_INCREMENT,"
                          "eqs_date DATETIME,"
                          "eqs_user INT default 0,"
                          "eqs_eqp INT NOT NULL,"
                          "eqs_operator INT NOT NULL,"
                          "eqs_comm text not null default '',"
                          "PRIMARY KEY (eqs_ser),"
                          "INDEX (eqs_eqp)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table eqp_preventive_maintenance,\n\terr=" + str(err))

    # Create table eqp_maintenance_contract
    try:
        conn.execute(text("create table if not exists eqp_maintenance_contract("
                          "eqc_ser int not NULL AUTO_INCREMENT,"
                          "eqc_date DATETIME,"
                          "eqc_user INT default 0,"
                          "eqc_eqp INT NOT NULL,"
                          "eqc_supplier INT NOT NULL,"
                          "eqc_date_upd DATETIME,"
                          "eqc_comm text not null default '',"
                          "PRIMARY KEY (eqc_ser),"
                          "INDEX (eqc_eqp)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table eqp_maintenance_contract,\n\terr=" + str(err))

    # ADD COLUMN for equipment critical
    try:
        conn.execute(text("alter table sigl_equipement_data add column eqp_critical varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column eqp_critical to sigl_equipement_data,\n\terr=" + str(err))

    # ADD COLUMN for equipment doc comment
    try:
        conn.execute(text("alter table sigl_equipement_data add column eqp_comm_doc text not null default ''"))
    except Exception as err:
        print("ERROR add column eqp_comm_doc to sigl_equipement_data,\n\terr=" + str(err))

    # CHANGE COLUMN date_dos to rec_date_receipt
    try:
        conn.execute(text("alter table sigl_02_data change column date_dos rec_date_receipt datetime"))
    except Exception as err:
        print("ERROR change column date_dos to sigl_02_data,\n\terr=" + str(err))

    # CHANGE COLUMN date_dos to rec_date_receipt in deleted table
    try:
        conn.execute(text("alter table sigl_02_deleted change column date_dos rec_date_receipt datetime"))
    except Exception as err:
        print("ERROR change column date_dos to sigl_02_deleted,\n\terr=" + str(err))

    # --- QUALITY EQUIPMENT DATA MIGRATION  ---
    # Migration to eqp_document
    l_eqp = conn.execute(text("select id_data, id_owner, manuel_id, procedures_id "
                              "from sigl_equipement_data "
                              "order by id_data asc"))

    rows = l_eqp.fetchall()

    for row in rows:
        param = {}
        param['user'] = row[1]
        param['eqp']  = row[0]

        # Manual attached to this equipment
        if row[2] and row[2] > 0:
            param['ref'] = row[2]
            try:
                conn.execute(text("insert into eqp_document (eqd_date, eqd_user, eqd_eqp, eqd_type, eqd_ref) "
                                  "values (NOW(), :user, :eqp, 'MANU', :ref)"), param)
            except Exception as err:
                print("ERROR migration manuel_id with insert into eqp_document,\n\terr=" + str(err))

        # Procedure attached to this equipment
        if row[3] and row[3] > 0:
            param['ref'] = row[3]
            try:
                conn.execute(text("insert into eqp_document (eqd_date, eqd_user, eqd_eqp, eqd_type, eqd_ref) "
                                  "values (NOW(), :user, :eqp, 'PROC', :ref)"), param)
            except Exception as err:
                print("ERROR migration procedure_id with insert into eqp_document,\n\terr=" + str(err))

    # Migration to preventive_maintenance
    l_comm = conn.execute(text("select date_format(lic_date, '%Y-%m-%d %H:%i:%s'), lic_user, lic_ref, lic_comm "
                               "from list_comment "
                               "where lic_type='E' and lic_sub_type='M' "
                               "order by lic_ser asc"))

    rows = l_comm.fetchall()

    for row in rows:
        param = {}
        param['date'] = str(row[0]) if row[0] else ''
        param['user'] = row[1] if row[1] else 0
        param['eqp']  = row[2] if row[2] else 0
        param['operator'] = param['user']
        param['comm'] = str(row[3]) if row[3] else ''

        try:
            conn.execute(text("insert into eqp_preventive_maintenance (eqs_date, eqs_user, eqs_eqp, eqs_operator, eqs_comm) "
                              "values (:date, :user, :eqp, :operator, :comm)"), param)
        except Exception as err:
            print("ERROR migration list_comment to insert into eqp_preventive_maintenance,\n\terr=" + str(err))

    # Migration update id_ext to eqp_preventive_maintenance_file
    l_eqs = conn.execute(text("select eqs_ser, eqs_eqp "
                              "from eqp_preventive_maintenance "
                              "order by eqs_ser asc"))

    rows = l_eqs.fetchall()

    for row in rows:
        param = {}
        param['eqs'] = row[0]
        param['eqp'] = row[1]
        try:
            conn.execute(text("update eqp_preventive_maintenance_file set id_ext = :eqs "
                              "where id_ext = :eqp"), param)
        except Exception as err:
            print("ERROR migration update id_ext into eqp_preventive_maintenance_file,\n\terr=" + str(err))

    # Migration to maintenance_contract
    l_eqp = conn.execute(text("select date_format(sys_creation_date, '%Y-%m-%d %H:%i:%s'), id_owner, id_data, "
                              "fournisseur_id, date_format(date_fin_contrat, '%Y-%m-%d'), contrat_maintenance "
                              "from sigl_equipement_data "
                              "order by id_data asc"))

    rows = l_eqp.fetchall()

    for row in rows:
        param = {}
        param['date'] = str(row[0]) if row[0] else ''
        param['user'] = row[1] if row[1] else 0
        param['eqp']  = row[2] if row[2] else 0
        param['supplier'] = row[3] if row[3] else 0
        param['date_upd'] = str(row[4]) if row[4] else ''
        param['comm'] = str(row[5]) if row[5] else ''

        try:
            conn.execute(text("insert into eqp_maintenance_contract (eqc_date, eqc_user, eqc_eqp, eqc_supplier, "
                              "eqc_date_upd, eqc_comm) "
                              "values (:date, :user, :eqp, :supplier, :date_upd, :comm)"), param)
        except Exception as err:
            print("ERROR migration contrat_maintenance to insert into eqp_maintenance_contract,\n\terr=" + str(err))

    # Migration update id_ext to eqp_maintenance_file
    l_eqc = conn.execute(text("select eqc_ser, eqc_eqp "
                              "from eqp_maintenance_contract "
                              "order by eqc_ser asc"))

    rows = l_eqc.fetchall()

    for row in rows:
        param = {}
        param['eqc'] = row[0]
        param['eqp'] = row[1]

        try:
            conn.execute(text("update eqp_maintenance_file set id_ext = :eqc "
                              "where id_ext = :eqp"), param)
        except Exception as err:
            print("ERROR migration update id_ext into eqp_maintenance_file,\n\terr=" + str(err))

    # Migration to eqp_failure
    l_comm = conn.execute(text("select date_format(lic_date, '%Y-%m-%d %H:%i:%s'), lic_user, lic_ref, lic_comm "
                               "from list_comment "
                               "where lic_type='E' and lic_sub_type='B' "
                               "order by lic_ser asc"))

    rows = l_comm.fetchall()

    for row in rows:
        param = {}
        param['date'] = str(row[0]) if row[0] else ''
        param['user'] = row[1] if row[1] else 0
        param['eqp']  = row[2] if row[2] else 0
        param['type'] = 'FAIL'
        param['supplier'] = 0
        param['incharge'] = param['user']
        param['comm'] = str(row[3]) if row[3] else ''

        try:
            eqp = conn.execute(text("select fournisseur_id "
                                    "from sigl_equipement_data "
                                    "where id_data= :eqp"), param)

            row_eqp = eqp.fetchone()

            if row_eqp and row_eqp[0] > 0:
                param['supplier'] = row_eqp[0]

            conn.execute(text("insert into eqp_failure (eqf_date, eqf_user, eqf_eqp, eqf_type, eqf_supplier, "
                              "eqf_incharge, eqf_comm) values "
                              "(:date, :user, :eqp, :type, :supplier, :incharge, :comm)"), param)
        except Exception as err:
            print("ERROR migration list_comment to insert into eqp_failure,\n\terr=" + str(err))

    # Migration update id_ext to eqp_preventive_maintenance_file
    l_eqf = conn.execute(text("select eqf_ser, eqf_eqp "
                              "from eqp_failure "
                              "order by eqf_ser asc"))

    rows = l_eqf.fetchall()

    for row in rows:
        param = {}
        param['eqf'] = row[0]
        param['eqp'] = row[1]

        try:
            conn.execute(text("update eqp_failure_file set id_ext = :eqf "
                              "where id_ext = :eqp"), param)
        except Exception as err:
            print("ERROR migration update id_ext into eqp_failure_file,\n\terr=" + str(err))

    # Migration to eqp_metrology
    l_eqp = conn.execute(text("select date_format(sys_creation_date, '%Y-%m-%d %H:%i:%s'), id_owner, id_data, "
                              "fournisseur_id, certif_etalonnage "
                              "from sigl_equipement_data "
                              "order by id_data asc"))

    rows = l_eqp.fetchall()

    for row in rows:
        param = {}
        param['date'] = str(row[0]) if row[0] else ''
        param['user'] = row[1] if row[1] else 0
        param['eqp']  = row[2] if row[2] else 0
        param['supplier'] = row[3] if row[3] else 0
        param['comm'] = str(row[4]) if row[4] else ''

        try:
            conn.execute(text("insert into eqp_metrology (eqm_date, eqm_user, eqm_eqp, eqm_supplier, eqm_comm) "
                              "values (:date, :user, :eqp, :supplier, :comm)"), param)
        except Exception as err:
            print("ERROR migration certif_etalonnage to insert into eqp_metrology,\n\terr=" + str(err))

    # Migration update id_ext to eqp_calibration_file
    l_eqm = conn.execute(text("select eqm_ser, eqm_eqp "
                              "from eqp_metrology "
                              "order by eqm_ser asc"))

    rows = l_eqm.fetchall()

    for row in rows:
        param = {}
        param['eqm'] = row[0]
        param['eqp'] = row[1]

        try:
            conn.execute(text("update eqp_calibration_file set id_ext = :eqm "
                              "where id_ext = :eqp"), param)
        except Exception as err:
            print("ERROR migration update id_ext into eqp_calibration_file,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_4_3_new_ui_equipment revision=e038e2ab0b42")


def downgrade():
    pass
