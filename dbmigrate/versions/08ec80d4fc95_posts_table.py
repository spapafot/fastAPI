"""posts table

Revision ID: 08ec80d4fc95
Revises: 
Create Date: 2022-01-07 10:02:08.404645

"""
from datetime import timezone
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '08ec80d4fc95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("email", sa.String(), nullable=False), 
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
    
                    )
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("titlle", sa.String(), nullable=False), 
                    sa.Column("content", sa.String(), nullable=False),
                    sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column("user_id", sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint("id")
                    )
    
    op.create_table("votes", 
                    sa.Column("post_id", sa.Integer(), nullable=False), 
                    sa.Column("user_id", sa.Integer(), nullable=False), 
                    sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint("post_id", "user_id")
                    )


def downgrade():
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('votes')
