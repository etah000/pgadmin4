
"""Added columns for SSH connection information

Revision ID: 5c96ef8fe45f
Revises: d39482714a2e
Create Date: 2021-01-27 18:24:08.002602

"""
from alembic import op
import sqlalchemy as sa
from pgadmin.model import db

# revision identifiers, used by Alembic.
revision = '5c96ef8fe45f'
down_revision = 'd39482714a2e'
branch_labels = None
depends_on = None


def upgrade():
    db.engine.execute(
        'ALTER TABLE server ADD COLUMN ssh_port INTEGER DEFAULT 0'
    )
    db.engine.execute(
        'ALTER TABLE server ADD COLUMN ssh_key_file TEXT'
    )
    db.engine.execute(
        'ALTER TABLE server ADD COLUMN ssh_username TEXT'
    )
    db.engine.execute(
        'ALTER TABLE server ADD COLUMN ssh_password TEXT'
    )
    db.engine.execute(
        'ALTER TABLE server ADD COLUMN ssh_authentication_type INTEGER DEFAULT 0'
    )

def downgrade():
    pass
