from flask import Flask, request, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from models import db, Paciente, Medico, Consulta
from datetime import datetime
import secrets

app = Flask(__name__)

# Gera uma chave secreta aleatória e define-a no aplicativo Flask
app.secret_key = secrets.token_hex(16)  # Gera uma chave secreta aleatória
print(f"Chave secreta gerada: {app.secret_key}")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa SQLAlchemy com o aplicativo
migrate = Migrate(app, db)  # Inicializa Flask-Migrate

@app.route('/')
def index():
    consultas = Consulta.query.all()
    return render_template('index.html', consultas=consultas)

@app.route('/cadastro_medico', methods=['GET', 'POST'])
def cadastro_medico():
    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        novo_medico = Medico(nome=nome, especialidade=especialidade)
        db.session.add(novo_medico)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro_medico.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento_str = request.form['data_nascimento']
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()  # Converte para objeto date
        telefone = request.form['telefone']
        endereco = request.form['endereco']

        novo_paciente = Paciente(nome=nome, data_nascimento=data_nascimento, telefone=telefone, endereco=endereco)
        db.session.add(novo_paciente)
        db.session.commit()
        return redirect(url_for('cadastro'))

    # Consultar todos os pacientes registados
    pacientes = Paciente.query.all()
    return render_template('cadastro_paciente.html', pacientes=pacientes)

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        try:
            data_hora_str = request.form['data_hora']
            paciente_id = request.form['paciente_id']
            medico_id = request.form['medico_id']

            # Converte a string da data e hora para um objeto datetime
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')

            nova_consulta = Consulta(data_hora=data_hora, paciente_id=paciente_id, medico_id=medico_id)
            db.session.add(nova_consulta)
            db.session.commit()

            return redirect(url_for('sucesso'))
        except Exception as e:
            print(f'Ocorreu um erro: {e}')
            return "Erro ao agendar a consulta."

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    return render_template('agendamento.html', pacientes=pacientes, medicos=medicos)

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')


@app.route('/remover/<int:paciente_id>', methods=['POST'])
def remover_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    if paciente:
        # Remover todas as consultas associadas a este paciente
        consultas = Consulta.query.filter_by(paciente_id=paciente_id).all()
        for consulta in consultas:
            db.session.delete(consulta)  # Remove cada consulta associada

        db.session.delete(paciente)  # Remove o paciente
        db.session.commit()
        flash('Paciente removido com sucesso!', 'success')
    else:
        flash('Paciente não encontrado.', 'danger')
    return redirect(url_for('cadastro'))

@app.route('/remover_consulta/<int:consulta_id>', methods=['POST'])
def remover_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)  # Obtém a consulta ou retorna 404 se não encontrar
    db.session.delete(consulta)  # Remove a consulta do banco de dados
    db.session.commit()  # Confirma a remoção
    flash('Consulta removida com sucesso!', 'success')  # Mensagem de confirmação
    return redirect(url_for('index'))  # Redireciona de volta para a página principal


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas, se ainda não existirem
    app.run(debug=True)
