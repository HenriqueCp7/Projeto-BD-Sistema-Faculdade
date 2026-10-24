from flask import Blueprint, jsonify, request
from ..database import (listar_associacoes, buscar_associacao as buscar_associacao_db, cadastrar_associacao, editar_associacao, deletar_associacao as deletar_associacao_db)

associacoes_bp = Blueprint("associacoes",__name__,url_prefix="/api/associacoes")

@associacoes_bp.route("/", methods=["GET"])
def buscar_associacoes():
    associacoes = listar_associacoes()

    resultado = []

    for associacao in associacoes:
        resultado.append({
            "id_professor": associacao[0],
            "nome_professor": associacao[1],
            "id_disciplina": associacao[2],
            "nome_disciplina": associacao[3],
            "carga_horaria": associacao[4]
        })

    return jsonify(resultado)


@associacoes_bp.route("/<int:id_professor>/<int:id_disciplina>",methods=["GET"])
def obter_associacao(id_professor, id_disciplina):
    associacao = buscar_associacao_db(id_professor, id_disciplina)

    if associacao is None:
        return jsonify({"erro": "Associação não encontrada"}), 404

    return jsonify({
        "id_professor": associacao[0],
        "id_disciplina": associacao[1],
        "carga_horaria": associacao[2]
    })


@associacoes_bp.route("/", methods=["POST"])
def criar_associacao():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados da associação em JSON"}), 400

    campos = [
        "id_professor",
        "id_disciplina",
        "carga_horaria"
    ]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    try:
        cadastrar_associacao(
            dados["id_professor"],
            dados["id_disciplina"],
            dados["carga_horaria"]
        )
    except Exception:
        return jsonify({
            "erro": "Não foi possível cadastrar a associação. Verifique os IDs e os dados enviados."
        }), 400

    return jsonify({"mensagem": "Associação cadastrada com sucesso"}), 201


@associacoes_bp.route("/<int:id_professor>/<int:id_disciplina>",methods=["PUT"])
def atualizar_associacao(id_professor, id_disciplina):
    dados = request.get_json()

    if not dados or "carga_horaria" not in dados:
        return jsonify({"erro": "Informe a carga_horaria em JSON"}), 400

    associacao = buscar_associacao_db(id_professor, id_disciplina)

    if associacao is None:
        return jsonify({"erro": "Associação não encontrada"}), 404

    try:
        editar_associacao(
            id_professor,
            id_disciplina,
            dados["carga_horaria"]
        )
    except Exception:
        return jsonify({"erro": "Não foi possível atualizar a associação."}), 400

    return jsonify({"mensagem": "Associação atualizada com sucesso"}), 200

@associacoes_bp.route("/<int:id_professor>/<int:id_disciplina>",methods=["DELETE"])
def deletar_associacao(id_professor, id_disciplina):
    associacao = buscar_associacao_db(id_professor, id_disciplina)

    if associacao is None:
        return jsonify({"erro": "Associação não encontrada"}), 404

    try:
        deletar_associacao_db(id_professor, id_disciplina)
    except Exception:
        return jsonify({"erro": "Não foi possível excluir a associação."}), 400

    return jsonify({"mensagem": "Associação excluída com sucesso"}), 200
