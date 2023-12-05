# Cria entidade aluno na plataforma

from flask import request, jsonify, make_response  # Importa o request, jsonify e make_response do flask
import utils  # Importa utils para gerar id
import professor  # Importa a entidade professor
import sqlite3   

app = Flask(__name__)

# Cria a entidade aluno

class Aluno(db.Model):
    __tablename__ = 'aluno'
    id = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.String(50), db.ForeignKey('professor.id'), nullable=False)
    professor = db.relationship('Professor', backref=db.backref('aluno', lazy=True))

    def __init__(self, nome, email, senha, professor_id):
        self.id = utils.generate_id()
        self.nome = nome
        self.email = email
        self.senha = senha
        self.professor_id = professor_id

    def __repr__(self):
        return '<Aluno %r>' % self.id

    # Cria aluno através da dados vindo do front-end via POST. Valida se aluno já existe
    def create_aluno():
        data = request.get_json()
        aluno = Aluno.query.filter_by(email=data['email']).first()
        if aluno:
            return make_response(jsonify({'message': 'Aluno já existe!'}), 400)
        else:
            aluno = Aluno(
                data['nome'],
                data['email'],
                data['senha'],
                data['professor_id']
            )
            db.session.add(aluno)
            db.session.commit()
            return make_response(jsonify({'message': 'Aluno criado com sucesso!'}), 201)
    
    # Lista todos os alunos através da dados vindo do front-end via GET
    def list_alunos():
        alunos = Aluno.query.all()
        return make_response(jsonify(alunos), 200)
    
    # Lista todos os alunos de um professor através da dados vindo do front-end via GET
    def list_alunos_professor(professor_id):
        alunos = Aluno.query.filter_by(professor_id=professor_id).all()
        return make_response(jsonify(alunos), 200)
    
    # Lista um aluno através da dados vindo do front-end via GET
    def list_aluno(id):
        aluno = Aluno.query.filter_by(id=id).first()
        return make_response(jsonify(aluno), 200)
    
    # Atualiza um aluno através da dados vindo do front-end via PUT
    def update_aluno(id):
        data = request.get_json()
        aluno = Aluno.query.filter_by(id=id).first()
        if aluno:
            aluno.nome = data['nome']
            aluno.email = data['email']
            aluno.senha = data['senha']
            aluno.professor_id = data['professor_id']
            db.session.commit()
            return make_response(jsonify({'message': 'Aluno atualizado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'message': 'Aluno não encontrado!'}), 404)

    # Deleta um aluno através da dados vindo do front-end via DELETE
    def delete_aluno(id):
        aluno = Aluno.query.filter_by(id=id).first()
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            return make_response(jsonify({'message': 'Aluno deletado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'message': 'Aluno não encontrado!'}), 404)
        
    # Autentica um aluno através da dados vindo do front-end via POST
    def login_aluno():
        data = request.get_json()
        aluno = Aluno.query.filter_by(email=data['email'], senha=data['senha']).first()
        if aluno:
            return make_response(jsonify({'message': 'Aluno autenticado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'message': 'Aluno não encontrado!'}), 404)
        

# Entradas de API RESTful para aluno

# Cria aluno através da dados vindo do front-end via POST
@app.route('/aluno', methods=['POST'])
def create_aluno():
    return Aluno.create_aluno()

# Lista todos os alunos através da dados vindo do front-end via GET
@app.route('/aluno', methods=['GET'])
def list_alunos():
    return Aluno.list_alunos()

# Lista todos os alunos de um professor através da dados vindo do front-end via GET
@app.route('/aluno/professor/<professor_id>', methods=['GET'])
def list_alunos_professor(professor_id):
    return Aluno.list_alunos_professor(professor_id)

# Lista um aluno através da dados vindo do front-end via GET
@app.route('/aluno/<id>', methods=['GET'])
def list_aluno(id):
    return Aluno.list_aluno(id)

# Atualiza um aluno através da dados vindo do front-end via PUT
@app.route('/aluno/<id>', methods=['PUT'])
def update_aluno(id):
    return Aluno.update_aluno(id)

# Deleta um aluno através da dados vindo do front-end via DELETE
@app.route('/aluno/<id>', methods=['DELETE'])
def delete_aluno(id):
    return Aluno.delete_aluno(id)

# Autentica um aluno através da dados vindo do front-end via POST
@app.route('/aluno/login', methods=['POST'])
def login_aluno():
    return Aluno.login_aluno()

# Roda a aplicação
if __name__ == '__main__':
    app.run(debug=True)
        