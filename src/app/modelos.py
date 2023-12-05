from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = 'users'
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
        return '<User %r>' % self.id

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
    
class Professor(db.Model):
    __tablename__ = 'professor'
    id = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    cref  = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, email, senha):
        self.id = utils.generate_id()
        self.nome = nome
        self.email = email
        self.senha = senha

    def __repr__(self):
        return '<Professor %r>' % self.id

    # Cria professor através da dados vindo do front-end via POST. Valida se professor já existe
    def create_professor():
        data = request.get_json()
        professor = Professor.query.filter_by(email=data['email']).first()
        if professor:
            return make_response(jsonify({'message': 'Professor já existe!'}), 400)
        else:
            professor = Professor(
                data['nome'],
                data['email'],
                data['senha']
            )
            db.session.add(professor)
            db.session.commit()
            return make_response(jsonify({'message': 'Professor criado com sucesso!'}), 201)
    
    # Lista todos os professores através da dados vindo do front-end via GET
    def list_professores():
        professores = Professor.query.all()
        return make_response(jsonify(professores), 200)
    
    # Lista um professor através da dados vindo do front-end via GET
    def list_professor(id):
        professor = Professor.query.filter_by(id=id).first()
        return make_response(jsonify(professor), 200)
    
    # Atualiza um professor através da dados vindo do front-end via PUT
    def update_professor(id):
        data = request.get_json()
        professor = Professor.query.filter_by(id=id).first()
        if professor:
            professor.nome = data['nome']
            professor.email = data['email']
            professor.senha = data['senha']
            professor.cref = data['cref']
            db.session.commit()
            return make_response(jsonify({'message': 'Professor atualizado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'message': 'Professor não encontrado!'}), 404)
        
    # Deleta um professor através da dados vindo do front-end via DELETE
    def delete_professor(id):
        professor = Professor.query.filter_by(id=id).first()
        if professor:
            db.session.delete(professor)
            db.session.commit()
            return make_response(jsonify({'message': 'Professor deletado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'message': 'Professor não encontrado!'}), 404)

class Plano(db.Model):
    __tablename__ = 'plano'
    id = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.String(50), db.ForeignKey('professor.id'), nullable=False)
    professor = db.relationship('Professor', backref=db.backref('plano', lazy=True))

    def __init__(self, nome, descricao, professor_id):
        self.id = utils.generate_id()
        self.nome = nome
        self.descricao = descricao
        self.professor_id = professor_id

    def __repr__(self):
        return '<Plano %r>' % self.id

    # Cria plano através da dados vindo do front-end via POST. Valida se plano já existe
    def create_plano():
        data = request.get_json()
        plano = Plano.query.filter_by(nome=data['nome']).first()
        if plano:
            return make_response(jsonify({'message': 'Plano já existe!'}), 400)
        else:
            plano = Plano(
                data['nome'],
                data['descricao'],
                data['professor_id']
            )
            db.session.add(plano)
            db.session.commit()
            return make_response(jsonify({'message': 'Plano criado com sucesso!'}), 201)
    
    # Lista todos os planos através da dados vindo do front-end via GET
    def list_planos():
        planos = Plano.query.all()
        return make_response(jsonify(planos), 200)
    
    # Lista todos os planos de um professor através da dados vindo do front-end via GET
    def list_planos_professor(professor_id):
        planos = Plano.query.filter_by(professor_id=professor_id).all()
        return make_response(jsonify(planos), 200)
    
    # Lista um plano através da dados vindo do front-end via GET
    def list_plano(id):
        plano = Plano.query.filter_by(id=id).first()
        return make_response(jsonify(plano), 200)
    
    # Atualiza um plano através da dados vindo do front-end via PUT
    def update_plano(id):
        data = request.get_json()
        plano = Plano.query.filter_by(id=id)
        if plano:
            plano.nome = data['nome']
            plano.descricao = data['descricao']
            db.session.commit()
            return make_response(jsonify({'message': 'Plano atualizado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'message': 'Plano não encontrado!'}), 404)