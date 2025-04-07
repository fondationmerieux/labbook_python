# -*- coding:utf-8 -*-
"""v3_5_8_various_things

Revision ID: ad1a2b5e4b10
Revises: 558a7ba02d35
Create Date: 2025-03-24 10:12:37.821201

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'ad1a2b5e4b10'
down_revision = '558a7ba02d35'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_5_8_various_things revision=ad1a2b5e4b10")

    import os

    # Create printer directory
    printer_path = '/storage/resource/printer'

    if not os.path.exists(printer_path):
        os.makedirs(printer_path, mode=0o777, exist_ok=True)
        os.chmod(printer_path, 0o777)

    # Get the current
    conn = op.get_bind()

    # Delete the manual titled "WHO Guidance on regulations for transport of infectious substances 2019"
    target_title = "WHO Guidance on regulations for transport of infectious substances 2019"

    # Fetch manual ID from sigl_manuels_data
    result = conn.execute(text("""
        SELECT id_data FROM sigl_manuels_data
        WHERE titre = :titre
    """), {"titre": target_title})
    row = result.fetchone()

    if row:
        manual_id = row[0]

        # Fetch file ID from manual_file using the manual ID as external reference
        result_file = conn.execute(text("""
            SELECT id_file FROM manual_file
            WHERE id_ext = :manual_id
        """), {"manual_id": manual_id})
        file_row = result_file.fetchone()

        if file_row:
            file_id = file_row[0]

            # Delete file data from sigl_file_data
            conn.execute(text("""
                DELETE FROM sigl_file_data
                WHERE id_data = :file_id
            """), {"file_id": file_id})

        # Delete the link between manual and file from manual_file
        conn.execute(text("""
            DELETE FROM manual_file
            WHERE id_ext = :manual_id
        """), {"manual_id": manual_id})

        # Finally, delete the manual entry itself
        conn.execute(text("""
            DELETE FROM sigl_manuels_data
            WHERE id_data = :manual_id
        """), {"manual_id": manual_id})
    else:
        print("Manual not found in sigl_manuels_data.")

    # Create table for printer_setting
    try:
        conn.execute(text('''
                          create table printer_setting(
                          prt_ser int not NULL AUTO_INCREMENT,
                          prt_date DATETIME,
                          prt_name varchar(100) not null,
                          prt_script varchar(255) not null,
                          prt_default varchar(1) not null default "N",
                          prt_rank int default 0,
                          PRIMARY KEY (prt_ser))
                          character set=utf8
                          '''))
    except Exception as err:
        print("ERROR create table printer_setting,\n\terr=" + str(err))

    # Add role agent for using mobile device
    try:
        conn.execute(text('''
                          insert into sigl_pj_role (name, label, type)
                          values ('agent', 'Agent', 'AGT')
                          '''))
    except Exception as err:
        print("ERROR insert into sigl_pj_role (Agent),\n\terr=" + str(err))

    # Insert profile role by default
    try:
        conn.execute(text('''
                          insert into profile_role (pro_date, pro_by_user, pro_role, pro_label, pro_genuine,
                          pro_color_1, pro_color_2, pro_text_color)
                          values (NOW(), 0, (select max(id_role) from sigl_pj_role), "Agent", "Y", "#FFFFFF",
                          "#E3E3E3", "#000000")
                          '''))

        # Fetch the last inserted pro_ser
        result = conn.execute(text('SELECT MAX(pro_ser) FROM profile_role'))
        pro_ser = result.scalar()
    except Exception as err:
        print("ERROR insert default profile_role for Agent,\n\terr=" + str(err))
        pro_ser = None

    # Insert default permissions for agent (pro_ser = 13)
    if pro_ser:
        try:
            permissions = ",".join([
                f"(NOW(), 0, {pro_ser}, {i}, 'N')" for i in range(1, 174)
            ])

            conn.execute(text(f'''
                              INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
                              VALUES {permissions}
                              '''))
        except Exception as err:
            print("ERROR insert default profile_permissions for Agent,\n\terr=" + str(err))

    # Create table for lite_setting
    try:
        conn.execute(text('''
                          create table lite_setting(
                          lite_ser int not NULL AUTO_INCREMENT,
                          lite_date DATETIME,
                          lite_name varchar(100) not null,
                          lite_login varchar(50) not null,
                          lite_pwd varchar(100) not null,
                          PRIMARY KEY (lite_ser))
                          character set=utf8
                          '''))
    except Exception as err:
        print("ERROR create table lite_setting,\n\terr=" + str(err))

    # Create table for lite_users
    try:
        conn.execute(text('''
                          create table lite_users(
                          litu_ser int not NULL AUTO_INCREMENT,
                          litu_date DATETIME,
                          litu_lite int not null,
                          litu_user int not null,
                          PRIMARY KEY (litu_ser), INDEX(litu_lite), INDEX(litu_user))
                          character set=utf8
                          '''))
    except Exception as err:
        print("ERROR create table lite_users,\n\terr=" + str(err))

    # ADD COLUMN for ana_lite in sigl_05_data
    try:
        conn.execute(text("alter table sigl_05_data add column ana_lite varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column ana_lite to sigl_05_data,\n\terr=" + str(err))

    # ADD COLUMN for pat_email in sigl_03_data
    try:
        conn.execute(text("alter table sigl_03_data add column pat_email varchar(255) not null default ''"))
    except Exception as err:
        print("ERROR add column pat_email to sigl_03_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_5_8_various_things revision=ad1a2b5e4b10")


def downgrade():
    pass
