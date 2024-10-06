from flask import Flask, request, render_template, redirect, url_for

from flask_migrate import Migrate
from models import db, Paciente, Medico, Consulta  # Ensure db is imported
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize SQLAlchemy with the app
migrate = Migrate(app, db)  # Initialize Flask-Migrate


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

        # Convert the date string to a date object
        data_nascimento_str = request.form['data_nascimento']  # Assuming the format is 'YYYY-MM-DD'
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()  # Convert to date object

        telefone = request.form['telefone']
        endereco = request.form['endereco']

        # Create a new Paciente object with the correct data types
        novo_paciente = Paciente(nome=nome, data_nascimento=data_nascimento, telefone=telefone, endereco=endereco)
        db.session.add(novo_paciente)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro_paciente.html')


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

            # Redireciona para a página de sucesso após o agendamento
            return redirect(url_for('sucesso'))

        except Exception as e:
            print(f'Ocorreu um erro: {e}')  # Para depuração
            return "Erro ao agendar a consulta."

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    return render_template('agendamento.html', pacientes=pacientes, medicos=medicos)


# Nova rota para a página de sucesso
@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables if not already created
    app.run(debug=True)
