from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

# Configuração do BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.sqlite3'


db = SQLAlchemy(app)

# Modelo do Banco
class Funcionario(db.Model):
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primeiro_nome   = db.Column(db.String(150), nullable=False)
    ultimo_nome     = db.Column(db.String(150), nullable=False)
    idade           = db.Column(db.Integer, nullable=False)
    CPF             = db.Column(db.Integer, nullable=False)
    cargo           = db.Column(db.String(150), nullable=False)
    salario         = db.Column(db.Integer, nullable=False)

# Crição da tabela dentro do app context
with app.app_context():
        db.create_all()         #Todas as tabelas (Estudante)


@app.route("/listar_funcionarios")
def home():
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios/listar_funcionarios.html', funcionarios=funcionarios)

@app.route("/add_funcionario", methods=["GET", "POST"]) # Indica que a rota aceita dois tipos de requisição: 
                                            # GET: Utilizado para recuperar dados e carregar páginas (como exibir um formulário), enviando informações pela URL.
                                            # POST: Usado para enviar dados ao servidor para processamento ou criação (como submeter formulários ou criar usuários), 
                                            # ocultando os dados no corpo da requisição, ideal para segurança e grandes quantidades de dados. 
def add():
    if request.method == "POST":    # Se o método da requisição for POST, é usado para acessar dados de solicitações HTTP (GET/POST) em funções de visualização.
        primeiro_nome = request.form.get("primeiro_nome")   # Captura o valor do formulário e armazena em uma variável
        ultimo_nome   = request.form.get("ultimo_nome")
        idade         = request.form.get("idade")
        CPF           = request.form.get("CPF")
        cargo         = request.form.get("cargo")
        salario       = request.form.get("salario")


        if primeiro_nome and ultimo_nome and idade:  # Realiza uma validação simples de presença de dados antes de tentar salvar as informações no banco de dados.
            f = Funcionario(
                primeiro_nome = primeiro_nome,
                ultimo_nome   = ultimo_nome,
                idade         = int(idade),
                CPF           = int(CPF),
                cargo         = cargo,
                salario       = int(salario)
            )
            db.session.add(f)
            db.session.commit()
            return redirect("/listar_funcionarios") # Redireciona para a rota "/" após salvar
    return render_template('funcionarios/add_funcionario.html')

if __name__ == ('__main__'):
    app.run(debug=True)
