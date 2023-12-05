from flask import Blueprint, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from src.app import modelos

main = Blueprint('main', __name__)

db = SQLAlchemy()

@main.route('/aluno', methods=['POST'])
def create_aluno():
    data = request.get_json()
    aluno = modelos.Aluno.query.filter_by(email=data['email']).first()
    if aluno:
        return make_response(jsonify({'message': 'Aluno já existe!'}), 400)
    else:
        aluno = modelos.Aluno(
            data['nome'],
            data['email'],
            data['senha'],
            data['professor_id']
        )
        db.session.add(aluno)
        db.session.commit()
        return make_response(jsonify({'message': 'Aluno criado com sucesso!'}), 201)

@main.route('/alunos', methods=['GET'])
def list_alunos():
    alunos = modelos.Aluno.query.all()
    return make_response(jsonify(alunos), 200)

@main.route('/alunos/<professor_id>', methods=['GET'])
def list_alunos_professor(professor_id):
    alunos = modelos.Aluno.query.filter_by(professor_id=professor_id).all()
    return make_response(jsonify(alunos), 200)

@main.route('/aluno/<id>', methods=['GET'])
def list_aluno(id):
    aluno = modelos.Aluno.query.filter_by(id=id).first()
    return make_response(jsonify(aluno), 200)

@main.route('/aluno/<id>', methods=['PUT'])
def update_aluno(id):
    data = request.get_json()
    aluno = modelos.Aluno.query.filter_by(id=id).first()
    if aluno:
        aluno.nome = data['nome']
        aluno.email = data['email']
        aluno.senha = data['senha']
        db.session.commit()
        return make_response(jsonify({'message': 'Aluno atualizado com sucesso!'}), 200)
    else:
        return make_response(jsonify({'message': 'Aluno não encontrado!'}), 404)

@main.route('/aluno/<id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = modelos.Aluno.query.filter_by(id=id).first()
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return make_response(jsonify({'message': 'Aluno deletado com sucesso!'}), 200)
    else:
        return make_response(jsonify({'message': 'Aluno não encontrado!'}), 404)

@main.route('/professor', methods=['POST'])
