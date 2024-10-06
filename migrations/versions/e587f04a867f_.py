"""empty message

Revision ID: e587f04a867f
Revises: 
Create Date: 2024-10-05 22:42:10.675037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e587f04a867f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('especialidade', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('paciente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('data_nascimento', sa.Date(), nullable=True),
    sa.Column('telefone', sa.String(length=15), nullable=True),
    sa.Column('endereco', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consulta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_hora', sa.DateTime(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.Column('medico_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['medico_id'], ['medico.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['paciente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('consulta')
    op.drop_table('paciente')
    op.drop_table('medico')
    # ### end Alembic commands ###
