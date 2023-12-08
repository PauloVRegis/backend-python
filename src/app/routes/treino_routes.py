from flask import Flask, Blueprint, jsonify, request

treino = Blueprint('treino', __name__)
treino_controller = TreinoController()

@treino_bp.route('/treino', methods=['POST'])
def criar_treino():
    data = request.get_json()
    novo_treino = treino_controller.criar_treino(data)
    return jsonify(novo_treino), 201

@treino_bp.route('/treino', methods=['GET'])
def listar_treino():
    treinos = treino_controller.listar_treino()
    return jsonify(treinos), 200

@treino_bp.route('/treino/<int:id>', methods=['GET'])
def buscar_treino(id):
    treino = treino_controller.buscar_treino(id)
    if treino_controller.buscar_treino(id) == False:
        return jsonify({'message': 'Treino não encontrado'}), 404
    return jsonify(treino), 200

@treino_bp.route('/treino/<int:id>', methods=['PUT'])
def atualizar_treino(id):
    data = request.get_json()
    treino = treino_controller.atualizar_treino(id, data)
    if treino_controller.atualizar_treino(id, data) == False:
        return jsonify({'message': 'Treino não encontrado'}), 404
    return jsonify(treino), 200

@treino_bp.route('/treino/<int:id>', methods=['DELETE'])
def deletar_treino(id):
    treino_controller.deletar_treino(id)
    if treino_controller.deletar_treino(id) == False:
        return jsonify({'message': 'Treino não encontrado'}), 404
    return jsonify({'message': 'Treino deletado com sucesso'}), 200
