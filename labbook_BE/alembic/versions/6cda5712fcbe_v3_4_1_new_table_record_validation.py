"""v3_4_1_new_table_record_validation

Revision ID: 6cda5712fcbe
Revises: b7e386aa17b1
Create Date: 2024-01-02 14:54:48.156515

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '6cda5712fcbe'
down_revision = 'b7e386aa17b1'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_4_1_new_table_record_validation revision=6cda5712fcbe")

    # Get the current
    conn = op.get_bind()

    # ADD COLUMN var_show_minmax
    try:
        conn.execute(text("alter table sigl_07_data add column var_show_minmax varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column var_show_minmax to sigl_07_data,\n\terr=" + str(err))

    # ADD COLUMN doc_zipcity
    try:
        conn.execute(text("alter table sigl_08_data add column doc_zipcity varchar(10) default ''"))
    except Exception as err:
        print("ERROR add column doc_zipcity to sigl_08_data,\n\terr=" + str(err))

    # ADD COLUMN rec_date_save
    try:
        conn.execute(text("alter table sigl_02_data add column rec_date_save datetime"))
    except Exception as err:
        print("ERROR add column rec_date_save to sigl_02_data,\n\terr=" + str(err))

    # update rec_save with date_dos
    try:
        conn.execute(text("update sigl_02_data set rec_date_save = date_dos"))
    except Exception as err:
        print("ERROR update rec_date,\n\terr=" + str(err))

    # ADD COLUMN rec_date_save for sigl_02_deleted
    try:
        conn.execute(text("alter table sigl_02_deleted add column rec_date_save datetime"))
    except Exception as err:
        print("ERROR add column rec_date_save to sigl_02_deleted,\n\terr=" + str(err))

    # Create table record_validation
    try:
        conn.execute(text("create table if not exists record_validation("
                          "rev_ser int not NULL AUTO_INCREMENT,"
                          "rev_date DATETIME,"
                          "rev_user INT default 0,"
                          "rev_rec INT default 0,"
                          "rev_comm text,"
                          "PRIMARY KEY (rev_ser),"
                          "INDEX (rev_user), INDEX (rev_rec)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table record_validation,\n\terr=" + str(err))

    # insert into record_validation, last comment validated for each record
    try:
        conn.execute(text("insert into record_validation (rev_date, rev_user, rev_rec, rev_comm) "
                          "select rev_date, rev_user, rev_rec, rev_comm "
                          "from ( "
                          "select vld.date_validation as rev_date, vld.id_owner as rev_user, rec.id_data as rev_rec, "
                          "vld.commentaire as rev_comm, "
                          "ROW_NUMBER() OVER (PARTITION BY rec.id_data ORDER BY vld.date_validation DESC) AS row_num "
                          "from sigl_02_data AS rec "
                          "inner join sigl_04_data AS req ON req.id_dos = rec.id_data "
                          "inner join sigl_09_data AS res ON res.id_analyse = req.id_data "
                          "inner join sigl_10_data AS vld ON vld.id_resultat = res.id_data and "
                          "vld.type_validation = 252 ) as RankedValidation where row_num=1"))
    except Exception as err:
        print("ERROR update record_validation,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_4_1_new_table_record_validation revision=6cda5712fcbe")


def downgrade():
    pass
