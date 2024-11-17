"""updated models

Revision ID: 5139cbd4df81
Revises: d7a5046c6785
Create Date: 2024-11-17 09:10:49.605258

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '5139cbd4df81'
down_revision = 'd7a5046c6785'
branch_labels = None
depends_on = None
from sqlalchemy.sql import text


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:

        index_list = op.get_bind().execute(text("PRAGMA index_list('course')"))
        if 'ix_course_semester' in [row[1] for row in index_list]:  # Access second element of each tuple
            batch_op.drop_index('ix_course_semester')
        #batch_op.drop_constraint('unique_course_entry', type_='unique')
        batch_op.create_unique_constraint('unique_course_entry', ['course_code'])
        batch_op.drop_column('time')
        batch_op.drop_column('location')
        batch_op.drop_column('section')
        batch_op.drop_column('semester')

    with op.batch_alter_table('course_professor', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('professor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('reviews')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_professor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reviews', sqlite.JSON(), nullable=True))
        batch_op.alter_column('professor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('semester', sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('section', sa.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column('location', sa.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('time', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_constraint('unique_course_entry', type_='unique')
        batch_op.create_unique_constraint('unique_course_entry', ['course_code', 'section', 'semester'])
        batch_op.create_index('ix_course_semester', ['semester'], unique=False)

    # ### end Alembic commands ###