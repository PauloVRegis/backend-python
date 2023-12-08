from flask import Flask, Blueprint, jsonify, request
from app.controllers.professor_controller import ProfessorController

professor = Blueprint('professor', __name__)
professor_controller = ProfessorController()

@professor.route('/professor', methods=['POST'])
def criar_professor():
    data = request.get_json()
    novo_professor = professor_controller.criar_professor(data)
    return jsonify(novo_professor), 201

@professor.route('/professor', methods=['GET'])
def listar_professor():
    professores = professor_controller.listar_professor()
    return jsonify(professores), 200

@professor.route('/professor/<int:id>', methods=['GET'])
def buscar_professor(id):
    professor = professor_controller.buscar_professor(id)
    if professor_controller.buscar_professor(id) == False:
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify(professor), 200

@professor.route('/professor/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    data = request.get_json()
    professor = professor_controller.atualizar_professor(id, data)
    if professor_controller.atualizar_professor(id, data) == False:
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify(professor), 200

@professor.route('/professor/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    professor_controller.deletar_professor(id)
    if professor_controller.deletar_professor(id) == False:
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify({'message': 'Professor deletado com sucesso'}), 200
