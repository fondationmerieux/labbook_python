# -*- coding:utf-8 -*-
"""v3_6_29_fhir_exchange

Revision ID: 7c1e5b93a4d2
Revises: 5960434beeb1
Create Date: 2026-10-18 09:00:00.000000

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

import secrets


# revision identifiers, used by Alembic.
revision = '7c1e5b93a4d2'
down_revision = '5960434beeb1'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_29_fhir_exchange revision=7c1e5b93a4d2")

    conn = op.get_bind()

    # Mapping between an external system reference and a LabBook object,
    # filled by the external API only, never by the laboratory staff
    try:
        conn.execute(text("create table external_ref("
                          "exr_ser int unsigned not NULL AUTO_INCREMENT,"
                          "exr_date DATETIME,"
                          "exr_by_user int default 0,"
                          "exr_type_ext varchar(255) NOT NULL,"
                          "exr_ref_ext varchar(128) NOT NULL,"
                          "exr_type_int varchar(20) NOT NULL,"
                          "exr_ref_int int unsigned NOT NULL,"
                          "PRIMARY KEY (exr_ser),"
                          "UNIQUE INDEX exr_external (exr_type_ext, exr_type_int, exr_ref_ext),"
                          "INDEX exr_internal (exr_type_int, exr_ref_int)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table external_ref,\n\terr=" + str(err))

    # LOINC code of a result variable, set on the analysis-variable link because the code
    # depends on the biological product of the analysis
    try:
        conn.execute(text("alter table sigl_05_07_data add column var_loinc varchar(20) default ''"))
    except Exception as err:
        print("ERROR add column var_loinc to sigl_05_07_data,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_05_07_data_test add column var_loinc varchar(20) default ''"))
    except Exception as err:
        print("ERROR add column var_loinc to sigl_05_07_data_test,\n\terr=" + str(err))

    # OAuth client of the Connect FHIR facade, with a secret of its own for each
    # laboratory, read in the OAuth client settings and copied into the fhir.toml of Connect
    try:
        exists = conn.execute(text(
            "SELECT 1 FROM oauth2_client WHERE oacl_client_id='labbook-connect-fhir' LIMIT 1"
        )).scalar()

        if not exists:
            conn.execute(text(
                "INSERT INTO oauth2_client ("
                " oacl_client_id, oacl_client_secret, oacl_client_name, oacl_user_id,"
                " oacl_redirect_uris, oacl_scope, oacl_grant_types, oacl_response_types,"
                " oacl_token_endpoint_auth_method, oacl_is_active) VALUES ("
                " 'labbook-connect-fhir', :secret, 'LabBook Connect FHIR', 0,"
                " '', 'external/analysis external/patient external/record external/result',"
                " 'client_credentials', 'code', 'client_secret_post', 'Y')"),
                {"secret": secrets.token_urlsafe(32)})
    except Exception as err:
        print("ERROR insert oauth2_client (connect fhir),\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_6_29_fhir_exchange revision=7c1e5b93a4d2")


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. To roll back, restore a verified backup
    taken before revision 7c1e5b93a4d2.
    """
    print("downgrade skipped: irreversible migration 7c1e5b93a4d2 (forward-only policy)")
