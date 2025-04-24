"""v3_5_9_before_iso_final

Revision ID: a6ade2bf2df6
Revises: ad1a2b5e4b10
Create Date: 2025-04-14 09:34:45.488389

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'a6ade2bf2df6'
down_revision = 'ad1a2b5e4b10'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_5_9_before_iso_final revision=a6ade2bf2df6")

    # Get the current
    conn = op.get_bind()

    # UPDATE COPY resource form patient with pat_email
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource/form/patient"
        toDirectory = "/storage/resource/form/patient"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR update copy alembic resource form patient with pat_email,\n\terr=" + str(err))

    # UPDATE switch Y to N some tech qualitician permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'TQ'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_38', 'SETTING_39', 'STOCK_139')
                          '''))
    except Exception as err:
        print("ERROR update tech qualitician Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # Insert profile rights
    try:
        conn.execute(text('''
                          insert into profile_rights (prr_ser, prr_date, prr_by_user, prr_rank, prr_type, prr_label, prr_tag)
                          values
                          (174, NOW(), 0, 29000,"PRINT","Configuration des imprimantes", "PRINT_174"),
                          (175, NOW(), 0, 30000,"LITE","Configuration LabBook Lite", "LITE_175")
                          '''))
    except Exception as err:
        print("ERROR insert new default profile_rights,\n\terr=" + str(err))

    # Insert default permissions to Y for Admin, Bio, Tech and Tech Advanced
    try:
        conn.execute(text('''
                          INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
                          SELECT NOW(), 0, profiles.prp_pro, prr.prr_ser, 'Y'
                          FROM profile_rights AS prr
                          JOIN (
                              SELECT 1 AS prp_pro
                              UNION SELECT 2
                              UNION SELECT 3
                              UNION SELECT 5
                          ) AS profiles
                          ON 1=1
                          WHERE prr.prr_ser BETWEEN 174 AND 175
                        '''))
    except Exception as err:
        print("ERROR inserting new default profile_permissions to Y for A, B, T, TA,\n\terr=" + str(err))

    # Insert default permissions to N for Others
    try:
        conn.execute(text('''
                          INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
                          SELECT NOW(), 0, profiles.prp_pro, prr.prr_ser, 'N'
                          FROM profile_rights AS prr
                          JOIN (
                              SELECT distinct pro_ser AS prp_pro
                              from profile_role
                              where pro_ser not in (1,2,3,5)
                          ) AS profiles
                          ON 1=1
                          WHERE prr.prr_ser BETWEEN 174 AND 175
                        '''))
    except Exception as err:
        print("ERROR inserting new default profile_permissions to N for others,\n\terr=" + str(err))

    # ADD COLUMN pat_lite
    try:
        conn.execute(text("alter table sigl_03_data add column pat_lite int not null default 0"))
    except Exception as err:
        print("ERROR add column pat_lite to sigl_03_data,\n\terr=" + str(err))

    # ADD COLUMN rec_lite
    try:
        conn.execute(text("alter table sigl_02_data add column rec_lite int not null default 0"))
    except Exception as err:
        print("ERROR add column rec_lite to sigl_02_data,\n\terr=" + str(err))

    # ADD COLUMN rec_num_lite
    try:
        conn.execute(text("alter table sigl_02_data add column rec_num_lite varchar(20) not null default ''"))
    except Exception as err:
        print("ERROR add column rec_num_lite to sigl_02_data,\n\terr=" + str(err))

    try:
        conn.execute(text("ALTER TABLE lite_setting ADD COLUMN lite_report_pwd VARCHAR(1) NOT NULL DEFAULT 'N'"))
    except Exception as err:
        print("ERROR add column lite_report_pwd to lite_setting,\n\terr=" + str(err))
    

    print(str(datetime.today()) + " : END of migration v3_5_9_before_iso_final revision=a6ade2bf2df6")


def downgrade():
    pass
