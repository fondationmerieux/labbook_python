# -*- coding:utf-8 -*-
"""v3_5_6_fix_role_rigths

Revision ID: 745df49ffe70
Revises: 2aff1c082bb7
Create Date: 2025-03-11 08:45:39.972429

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '745df49ffe70'
down_revision = '2aff1c082bb7'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration V3_5_6_fix_role_rigths revision=745df49ffe70")

    # Get the current
    conn = op.get_bind()

    # ADD COLUMN for sal_stock_date in storage_aliquot
    try:
        conn.execute(text("ALTER TABLE storage_aliquot ADD COLUMN sal_stock_date datetime default null"))
    except Exception as err:
        print("ERROR add column sal_stock_date to storage_aliquot,\n\terr=" + str(err))

    # Insert default permissions for API (pro_ser = 2)
    try:
        conn.execute(text('insert into profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted) '
                          'values '
                          '(NOW(), 0, 2, 1,"N"),'
                          '(NOW(), 0, 2, 2,"Y"),'
                          '(NOW(), 0, 2, 3,"N"),'
                          '(NOW(), 0, 2, 4,"N"),'
                          '(NOW(), 0, 2, 5,"N"),'
                          '(NOW(), 0, 2, 6,"N"),'
                          '(NOW(), 0, 2, 7,"N"),'
                          '(NOW(), 0, 2, 8,"N"),'
                          '(NOW(), 0, 2, 9,"N"),'
                          '(NOW(), 0, 2, 10,"N"),'
                          '(NOW(), 0, 2, 11,"N"),'
                          '(NOW(), 0, 2, 12,"N"),'
                          '(NOW(), 0, 2, 13,"N"),'
                          '(NOW(), 0, 2, 14,"N"),'
                          '(NOW(), 0, 2, 15,"N"),'
                          '(NOW(), 0, 2, 16,"N"),'
                          '(NOW(), 0, 2, 17,"N"),'
                          '(NOW(), 0, 2, 18,"N"),'
                          '(NOW(), 0, 2, 19,"N"),'
                          '(NOW(), 0, 2, 20,"N"),'
                          '(NOW(), 0, 2, 21,"N"),'
                          '(NOW(), 0, 2, 22,"N"),'
                          '(NOW(), 0, 2, 23,"N"),'
                          '(NOW(), 0, 2, 24,"N"),'
                          '(NOW(), 0, 2, 25,"N"),'
                          '(NOW(), 0, 2, 26,"N"),'
                          '(NOW(), 0, 2, 27,"N"),'
                          '(NOW(), 0, 2, 28,"N"),'
                          '(NOW(), 0, 2, 29,"N"),'
                          '(NOW(), 0, 2, 30,"N"),'
                          '(NOW(), 0, 2, 31,"N"),'
                          '(NOW(), 0, 2, 32,"N"),'
                          '(NOW(), 0, 2, 33,"N"),'
                          '(NOW(), 0, 2, 34,"N"),'
                          '(NOW(), 0, 2, 35,"N"),'
                          '(NOW(), 0, 2, 36,"N"),'
                          '(NOW(), 0, 2, 37,"N"),'
                          '(NOW(), 0, 2, 38,"N"),'
                          '(NOW(), 0, 2, 39,"N"),'
                          '(NOW(), 0, 2, 40,"N"),'
                          '(NOW(), 0, 2, 41,"N"),'
                          '(NOW(), 0, 2, 42,"N"),'
                          '(NOW(), 0, 2, 43,"N"),'
                          '(NOW(), 0, 2, 44,"N"),'
                          '(NOW(), 0, 2, 45,"N"),'
                          '(NOW(), 0, 2, 46,"N"),'
                          '(NOW(), 0, 2, 47,"N"),'
                          '(NOW(), 0, 2, 48,"N"),'
                          '(NOW(), 0, 2, 49,"N"),'
                          '(NOW(), 0, 2, 50,"N"),'
                          '(NOW(), 0, 2, 51,"N"),'
                          '(NOW(), 0, 2, 52,"N"),'
                          '(NOW(), 0, 2, 53,"N"),'
                          '(NOW(), 0, 2, 54,"N"),'
                          '(NOW(), 0, 2, 55,"N"),'
                          '(NOW(), 0, 2, 56,"N"),'
                          '(NOW(), 0, 2, 57,"N"),'
                          '(NOW(), 0, 2, 58,"N"),'
                          '(NOW(), 0, 2, 59,"N"),'
                          '(NOW(), 0, 2, 60,"N"),'
                          '(NOW(), 0, 2, 61,"N"),'
                          '(NOW(), 0, 2, 62,"N"),'
                          '(NOW(), 0, 2, 63,"N"),'
                          '(NOW(), 0, 2, 64,"N"),'
                          '(NOW(), 0, 2, 65,"N"),'
                          '(NOW(), 0, 2, 66,"N"),'
                          '(NOW(), 0, 2, 67,"N"),'
                          '(NOW(), 0, 2, 68,"N"),'
                          '(NOW(), 0, 2, 69,"N"),'
                          '(NOW(), 0, 2, 70,"N"),'
                          '(NOW(), 0, 2, 71,"N"),'
                          '(NOW(), 0, 2, 72,"N"),'
                          '(NOW(), 0, 2, 73,"N"),'
                          '(NOW(), 0, 2, 74,"N"),'
                          '(NOW(), 0, 2, 75,"N"),'
                          '(NOW(), 0, 2, 76,"N"),'
                          '(NOW(), 0, 2, 77,"N"),'
                          '(NOW(), 0, 2, 78,"N"),'
                          '(NOW(), 0, 2, 79,"N"),'
                          '(NOW(), 0, 2, 80,"N"),'
                          '(NOW(), 0, 2, 81,"N"),'
                          '(NOW(), 0, 2, 82,"N"),'
                          '(NOW(), 0, 2, 83,"N"),'
                          '(NOW(), 0, 2, 84,"N"),'
                          '(NOW(), 0, 2, 85,"N"),'
                          '(NOW(), 0, 2, 86,"N"),'
                          '(NOW(), 0, 2, 87,"N"),'
                          '(NOW(), 0, 2, 88,"N"),'
                          '(NOW(), 0, 2, 89,"N"),'
                          '(NOW(), 0, 2, 90,"N"),'
                          '(NOW(), 0, 2, 91,"N"),'
                          '(NOW(), 0, 2, 92,"N"),'
                          '(NOW(), 0, 2, 93,"N"),'
                          '(NOW(), 0, 2, 94,"N"),'
                          '(NOW(), 0, 2, 95,"N"),'
                          '(NOW(), 0, 2, 96,"N"),'
                          '(NOW(), 0, 2, 97,"N"),'
                          '(NOW(), 0, 2, 98,"N"),'
                          '(NOW(), 0, 2, 99,"N"),'
                          '(NOW(), 0, 2, 100,"N"),'
                          '(NOW(), 0, 2, 101,"N"),'
                          '(NOW(), 0, 2, 102,"N"),'
                          '(NOW(), 0, 2, 103,"N"),'
                          '(NOW(), 0, 2, 104,"N"),'
                          '(NOW(), 0, 2, 105,"N"),'
                          '(NOW(), 0, 2, 106,"N"),'
                          '(NOW(), 0, 2, 107,"N"),'
                          '(NOW(), 0, 2, 108,"N"),'
                          '(NOW(), 0, 2, 109,"N"),'
                          '(NOW(), 0, 2, 110,"N"),'
                          '(NOW(), 0, 2, 111,"N"),'
                          '(NOW(), 0, 2, 112,"N"),'
                          '(NOW(), 0, 2, 113,"N"),'
                          '(NOW(), 0, 2, 114,"N"),'
                          '(NOW(), 0, 2, 115,"N"),'
                          '(NOW(), 0, 2, 116,"N"),'
                          '(NOW(), 0, 2, 117,"N"),'
                          '(NOW(), 0, 2, 118,"N"),'
                          '(NOW(), 0, 2, 119,"N"),'
                          '(NOW(), 0, 2, 120,"N"),'
                          '(NOW(), 0, 2, 121,"N"),'
                          '(NOW(), 0, 2, 122,"N"),'
                          '(NOW(), 0, 2, 123,"N"),'
                          '(NOW(), 0, 2, 124,"N"),'
                          '(NOW(), 0, 2, 125,"N"),'
                          '(NOW(), 0, 2, 126,"N"),'
                          '(NOW(), 0, 2, 127,"N"),'
                          '(NOW(), 0, 2, 128,"N"),'
                          '(NOW(), 0, 2, 129,"N"),'
                          '(NOW(), 0, 2, 130,"N"),'
                          '(NOW(), 0, 2, 131,"N"),'
                          '(NOW(), 0, 2, 132,"N"),'
                          '(NOW(), 0, 2, 133,"N"),'
                          '(NOW(), 0, 2, 134,"N"),'
                          '(NOW(), 0, 2, 135,"N"),'
                          '(NOW(), 0, 2, 136,"N"),'
                          '(NOW(), 0, 2, 137,"N"),'
                          '(NOW(), 0, 2, 138,"N"),'
                          '(NOW(), 0, 2, 139,"N"),'
                          '(NOW(), 0, 2, 140,"N"),'
                          '(NOW(), 0, 2, 141,"N"),'
                          '(NOW(), 0, 2, 142,"N"),'
                          '(NOW(), 0, 2, 143,"N"),'
                          '(NOW(), 0, 2, 144,"N"),'
                          '(NOW(), 0, 2, 145,"N"),'
                          '(NOW(), 0, 2, 146,"N"),'
                          '(NOW(), 0, 2, 147,"N"),'
                          '(NOW(), 0, 2, 148,"N"),'
                          '(NOW(), 0, 2, 149,"N"),'
                          '(NOW(), 0, 2, 150,"N"),'
                          '(NOW(), 0, 2, 151,"N"),'
                          '(NOW(), 0, 2, 152,"N"),'
                          '(NOW(), 0, 2, 153,"N"),'
                          '(NOW(), 0, 2, 154,"N"),'
                          '(NOW(), 0, 2, 155,"N"),'
                          '(NOW(), 0, 2, 156,"N"),'
                          '(NOW(), 0, 2, 157,"N"),'
                          '(NOW(), 0, 2, 158,"N"),'
                          '(NOW(), 0, 2, 159,"N"),'
                          '(NOW(), 0, 2, 160,"N"),'
                          '(NOW(), 0, 2, 161,"N"),'
                          '(NOW(), 0, 2, 162,"N"),'
                          '(NOW(), 0, 2, 163,"N"),'
                          '(NOW(), 0, 2, 164,"N"),'
                          '(NOW(), 0, 2, 165,"N"),'
                          '(NOW(), 0, 2, 166,"N"),'
                          '(NOW(), 0, 2, 167,"N"),'
                          '(NOW(), 0, 2, 168,"N"),'
                          '(NOW(), 0, 2, 169,"N"),'
                          '(NOW(), 0, 2, 170,"N"),'
                          '(NOW(), 0, 2, 171,"N"),'
                          '(NOW(), 0, 2, 172,"N"),'
                          '(NOW(), 0, 2, 173,"N")'
                          ))
    except Exception as err:
        print("ERROR insert default profile_role API,\n\terr=" + str(err))

    # UPDATE switch Y to N some admin permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'A'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('API_2')
                          '''))
    except Exception as err:
        print("ERROR update admin Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some biologist permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'B'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_60', 'SETTING_61', 'SETTING_62', 'SETTING_63')
                          '''))
    except Exception as err:
        print("ERROR update biologist Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some biologist permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'Y'
                          WHERE r.type = 'B'
                          AND pp.prp_granted = 'N'
                          AND prr.prr_tag IN ('PROCEDURE_127')
                          '''))
    except Exception as err:
        print("ERROR update biologist N to Y profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some advanced technician permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'TA'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_71')
                          '''))
    except Exception as err:
        print("ERROR update advanced technician Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some technician qualitician permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'Y'
                          WHERE r.type = 'TQ'
                          AND pp.prp_granted = 'N'
                          AND prr.prr_tag IN ('STOCK_139')
                          '''))
    except Exception as err:
        print("ERROR update technician qualitician N to Y profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some stock manager permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'K'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('DOCTOR_87', 'DOCTOR_88', 'DOCTOR_89', 'DOCTOR_90')
                          '''))
    except Exception as err:
        print("ERROR update stock manager Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some qualitician permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'Q'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_60', 'SETTING_61', 'SETTING_62', 'SETTING_63')
                          '''))
    except Exception as err:
        print("ERROR update qualitician Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some prescriber permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'P'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('RECORD_15')
                          '''))
    except Exception as err:
        print("ERROR update prescriber Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some prescriber permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'Y'
                          WHERE r.type = 'P'
                          AND pp.prp_granted = 'N'
                          AND prr.prr_tag IN ('NONCONF_143', 'NONCONF_144', 'NONCONF_145', 'NONCONF_146')
                          '''))
    except Exception as err:
        print("ERROR update prescriber Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some laboratory permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'L'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('EQP_114')
                          '''))
    except Exception as err:
        print("ERROR update laboratory Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some aliquot permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type in ('A', 'SP', 'SA', 'S', 'K', 'P', 'L')
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('ALIQUOT_169', 'ALIQUOT_170', 'ALIQUOT_171', 'ALIQUOT_172', 'ALIQUOT_173')
                          '''))
    except Exception as err:
        print("ERROR update aliquot Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration V3_5_6_fix_role_rigths revision=745df49ffe70")


def downgrade():
    pass
