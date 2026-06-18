"""v3_6_20_fix_epidemio

Revision ID: 1d7606550c77
Revises: 2c884d401740
Create Date: 2026-06-18 09:09:05.058910

"""
from alembic import op
from sqlalchemy import text
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '1d7606550c77'
down_revision = '2c884d401740'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_20_fix_epidemio revision=1d7606550c77")

    conn = op.get_bind()

    # Copy alembic resources to /storage/resource
    # Update file only if source is newer
    try:
        import os
        import shutil

        sourceDirectory = "alembic/resource"
        destinationDirectory = "/storage/resource"

        # Create destination root if missing
        os.makedirs(destinationDirectory, exist_ok=True)

        # Walk through source directory tree
        for sourceRoot, sourceDirectories, sourceFiles in os.walk(sourceDirectory):

            # Keep directory structure
            relativePath = os.path.relpath(sourceRoot, sourceDirectory)
            destinationRoot = destinationDirectory if relativePath == "." else os.path.join(destinationDirectory, relativePath)

            # Create destination directory if missing
            os.makedirs(destinationRoot, exist_ok=True)

            # Copy file if missing or older than source
            for sourceFilename in sourceFiles:
                sourceFilePath = os.path.join(sourceRoot, sourceFilename)
                destinationFilePath = os.path.join(destinationRoot, sourceFilename)

                if not os.path.exists(destinationFilePath):
                    shutil.copy2(sourceFilePath, destinationFilePath)
                else:
                    sourceMtime = os.path.getmtime(sourceFilePath)  # source file modification time
                    destinationMtime = os.path.getmtime(destinationFilePath)

                    if sourceMtime > destinationMtime:
                        shutil.copy2(sourceFilePath, destinationFilePath)

    except Exception as err:
        print("ERROR copy alembic resource,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_6_20_fix_epidemio revision=1d7606550c77")


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. It includes destructive operations and/or renames
    that cannot be safely undone. To roll back, restore a verified backup
    taken before revision 1d7606550c77.
    """
    print("downgrade skipped: irreversible migration 1d7606550c77 (forward-only policy)")
