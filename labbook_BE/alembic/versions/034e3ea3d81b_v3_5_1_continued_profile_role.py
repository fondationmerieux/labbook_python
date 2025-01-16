# -*- coding:utf-8 -*-
"""v3_5_1_continued_profile_role

Revision ID: 034e3ea3d81b
Revises: ace6cf29d8ac
Create Date: 2025-01-07 16:10:45.716770

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '034e3ea3d81b'
down_revision = 'ace6cf29d8ac'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_5_1_continued_profile_role revision=034e3ea3d81b")

    # Get the current
    conn = op.get_bind()

    # COPY alembic resource
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource"
        toDirectory = "/storage/resource"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource,\n\terr=" + str(err))

    # ADD COLUMN for pro_genuine in profile_role to protect genuine role
    try:
        conn.execute(text("alter table profile_role add column pro_genuine varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column pro_genuine to profile_role,\n\terr=" + str(err))

    # UPDATE pro_genuine
    try:
        conn.execute(text("update profile_role set pro_genuine = 'Y' "
                          "where pro_ser < 14"))
    except Exception as err:
        print("ERROR update profile_role set pro_genuine to 'Y',\n\terr=" + str(err))

    # ADD COLUMN for prr_tag in profile_rigths to call permission easily
    try:
        conn.execute(text("alter table profile_rights add column prr_tag varchar(40) not null default ''"))
    except Exception as err:
        print("ERROR add column prr_tag to profile_rights,\n\terr=" + str(err))

    # UPDATE prr_tag
    try:
        conn.execute(text("update profile_rights set prr_tag = CONCAT(prr_type, '_', prr_ser)"))
    except Exception as err:
        print("ERROR update profile_rights set prr_tag to CONCAT(prr_type, '_', prr_ser),\n\terr=" + str(err))

    # UPDATE label of rights interne by externe for prr_ser in (158 to 162)
    try:
        conn.execute(text("update profile_rights set prr_label = replace(prr_label, 'interne', 'externe') "
                          "where prr_ser between 158 and 162"))
    except Exception as err:
        print("ERROR update profile_rights set prr_label repalce interne by externe,\n\terr=" + str(err))

    # ADD COLUMN for pro_color_1 in profile_role
    try:
        conn.execute(text("alter table profile_role add column pro_color_1 varchar(10) not null default '#EEEEEE'"))
    except Exception as err:
        print("ERROR add column pro_color_1 to profile_role,\n\terr=" + str(err))

    # ADD COLUMN for pro_color_2 in profile_role
    try:
        conn.execute(text("alter table profile_role add column pro_color_2 varchar(10) not null default '#DDDDDD'"))
    except Exception as err:
        print("ERROR add column pro_color_2 to profile_role,\n\terr=" + str(err))

    # ADD COLUMN for pro_text_color in profile_role
    try:
        conn.execute(text("alter table profile_role add column pro_text_color varchar(10) not null default '#FFFFFF'"))
    except Exception as err:
        print("ERROR add column pro_text_color to profile_role,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine for admin
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#FFCC00', pro_color_2='#E89400', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label ='Administrateur' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set admin pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine for biologist
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#8330E2', pro_color_2='#42159B', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label ='Biologiste' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set biologist pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine for stock manager
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#452ED1', pro_color_2='#292EBE', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label ='Gestionnaire de stock' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set stock pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine for laboratory
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#BB2688', pro_color_2='#A52396', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label ='Laboratoire' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set lab pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine for prescriber
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#996633', pro_color_2='#623201', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label ='Prescripteur' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set prescriber pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine for qualitician
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#E23176', pro_color_2='#AB2759', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label ='Qualiticien' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set qualitician pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine like secretary
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#EF8839', pro_color_2='#D36818', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label like 'Secr%' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set tech pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # UPDATE default colors for profile_role genuine like technician
    try:
        conn.execute(text("update profile_role set pro_color_1 = '#29B4ED', pro_color_2='#1499D2', "
                          "pro_text_color='#FFFFFF' "
                          "where pro_label like 'Technicien%' and pro_genuine='Y'"))
    except Exception as err:
        print("ERROR update profile_role set tech pro_color_1, pro_color_2, pro_text_color,\n\terr=" + str(err))

    # ADD template invoice
    try:
        conn.execute(text("insert into template_setting "
                          "(tpl_date, tpl_name, tpl_file, tpl_default, tpl_type) "
                          "values (NOW(), 'Modèle facturation', 'tpl_invoice.odt', 'Y', 'INV')"))
    except Exception as err:
        print("ERROR insert invoice template for template_setting,\n\terr=" + str(err))

    # ADD NEW USER ROLE
    try:
        conn.execute(text("insert into sigl_pj_role (name, label, type) "
                          "values ('préleveur', 'Préleveur', 'SP')"))
    except Exception as err:
        print("ERROR insert into sigl_pj_role (Préleveur),\n\terr=" + str(err))

    # Insert profile role by default
    try:
        conn.execute(text('insert into profile_role (pro_date, pro_by_user, pro_role, pro_label, pro_genuine, '
                          'pro_color_1, pro_color_2, pro_text_color) '
                          'values (NOW(), 0, (select max(id_role) from sigl_pj_role), "Préleveur", "Y", "#66994F", '
                          '"#3D5B2F", "#FFFFFF")'))
    except Exception as err:
        print("ERROR insert default profile_role for Préleveur,\n\terr=" + str(err))

    # Insert default permissions for Sampler (pro_ser = last id from profile_role)
    try:
        conn.execute(text('insert into profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted) '
                          'values '
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 1,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 2,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 3,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 4,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 5,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 6,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 7,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 8,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 9,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 10,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 11,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 12,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 13,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 14,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 15,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 16,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 17,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 18,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 19,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 20,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 21,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 22,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 23,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 24,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 25,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 26,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 27,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 28,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 29,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 30,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 31,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 32,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 33,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 34,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 35,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 36,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 37,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 38,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 39,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 40,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 41,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 42,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 43,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 44,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 45,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 46,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 47,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 48,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 49,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 50,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 51,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 52,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 53,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 54,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 55,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 56,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 57,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 58,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 59,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 60,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 61,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 62,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 63,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 64,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 65,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 66,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 67,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 68,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 69,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 70,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 71,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 72,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 73,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 74,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 75,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 76,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 77,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 78,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 79,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 80,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 81,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 82,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 83,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 84,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 85,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 86,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 87,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 88,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 89,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 90,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 91,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 92,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 93,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 94,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 95,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 96,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 97,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 98,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 99,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 100,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 101,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 102,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 103,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 104,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 105,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 106,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 107,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 108,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 109,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 110,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 111,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 112,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 113,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 114,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 115,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 116,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 117,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 118,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 119,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 120,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 121,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 122,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 123,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 124,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 125,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 126,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 127,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 128,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 129,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 130,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 131,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 132,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 133,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 134,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 135,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 136,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 137,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 138,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 139,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 140,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 141,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 142,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 143,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 144,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 145,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 146,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 147,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 148,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 149,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 150,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 151,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 152,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 153,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 154,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 155,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 156,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 157,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 158,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 159,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 160,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 161,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 162,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 163,"Y"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 164,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 165,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 166,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 167,"N"),'
                          '(NOW(), 0, (select max(pro_ser) from profile_role), 168,"N")'               
                          ))
    except Exception as err:
        print("ERROR insert default profile_role Sampler,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_5_1_continued_profile_role revision=034e3ea3d81b")


def downgrade():
    pass
