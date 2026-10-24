from flask import Blueprint, jsonify, request
from ..database import listar_disciplinas, buscar_disciplina as buscar_disciplina_db, cadastrar_disciplina, editar_disciplina, deletar_disciplina as deletar_disciplina_db

disciplinas_bp = Blueprint("disciplinas", __name__, url_prefix="/api/disciplinas")


@disciplinas_bp.route("/", methods=["GET"])
def buscar_disciplinas():
    disciplinas = listar_disciplinas()

    resultado = []

    for disciplina in disciplinas:
        resultado.append({
            "id_disciplina": disciplina[0],
            "nome_disciplina": disciplina[1],
            "carga_horaria": disciplina[2],
            "id_curso": disciplina[3],
            "nome_curso": disciplina[4],
        })

    return jsonify(resultado)

@disciplinas_bp.route("/<int:id_disciplina>", methods=["GET"])
def buscar_disciplina(id_disciplina):
    disciplina = buscar_disciplina_db(id_disciplina)

    if disciplina is None:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    return jsonify({
        "id_disciplina": disciplina[0],
        "nome_disciplina": disciplina[1],
        "carga_horaria": disciplina[2],
        "id_curso": disciplina[3],
        "nome_curso": disciplina[4],
    })

@disciplinas_bp.route("/", methods=["POST"])
def criar_disciplina():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados da disciplina em JSON"}), 400

    campos = [
        "nome_disciplina",
        "carga_horaria",
        "id_curso",
    ]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    try:
        cadastrar_disciplina(
            dados["nome_disciplina"],
            dados["carga_horaria"],
            dados["id_curso"],
        )
    except Exception:
        return jsonify({"erro": "Não foi possível cadastrar a disciplina. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Disciplina cadastrado com sucesso"}), 201

@disciplinas_bp.route("/<int:id_disciplina>", methods=["PUT"])
def atualizar_disciplina(id_disciplina):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados da disciplina em JSON"}), 400

    campos = ["nome_disciplina", "carga_horaria", "id_curso"]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    disciplina = buscar_disciplina_db(id_disciplina)

    if disciplina is None:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    try:
        editar_disciplina(
            id_disciplina,
            dados["nome_disciplina"],
            dados["carga_horaria"],
            dados["id_curso"],
        )
    except Exception:
        return jsonify({"erro": "Não foi possível atualizar a disciplina. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Disciplina atualizado com sucesso"}), 200

@disciplinas_bp.route("/<int:id_disciplina>", methods=["DELETE"])
def deletar_disciplina(id_disciplina):
    disciplina = buscar_disciplina_db(id_disciplina)

    if disciplina is None:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    try:
        deletar_disciplina_db(id_disciplina)
    except Exception:
        return jsonify({"erro": "Não foi possível excluir a disciplina."}), 400

    return jsonify({"mensagem": "Discilpina excluída com sucesso"}), 200

