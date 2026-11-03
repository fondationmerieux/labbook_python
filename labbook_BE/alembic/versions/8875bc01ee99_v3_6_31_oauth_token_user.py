# -*- coding:utf-8 -*-
"""v3_6_31_oauth_token_user

Revision ID: 8875bc01ee99
Revises: 7c1e5b93a4d2
Create Date: 2026-11-03 09:00:00.000000

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = '8875bc01ee99'
down_revision = '7c1e5b93a4d2'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_31_oauth_token_user revision=8875bc01ee99")

    conn = op.get_bind()

    # User of the authorization code
    try:
        conn.execute(text("alter table oauth2_code "
                          "add column oaco_user_id int unsigned NOT NULL DEFAULT 0 after oaco_client_id"))
    except Exception as err:
        print("ERROR add column oauth2_code.oaco_user_id,\n\terr=" + str(err))

    # User of the token, or 0 for a program without user
    try:
        conn.execute(text("alter table oauth2_token "
                          "add column oato_user_id int unsigned NOT NULL DEFAULT 0 after oato_client_id"))
    except Exception as err:
        print("ERROR add column oauth2_token.oato_user_id,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_6_31_oauth_token_user revision=8875bc01ee99")


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. To roll back, restore a verified backup
    taken before revision 8875bc01ee99.
    """
    print("downgrade skipped: irreversible migration 8875bc01ee99 (forward-only policy)")
