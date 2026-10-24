from flask import Blueprint, jsonify, request
from ..database import listar_professores, buscar_professor as buscar_professor_db, cadastrar_professor, editar_professor, deletar_professor as deletar_professor_db

professores_bp = Blueprint("professores", __name__, url_prefix="/api/professores")


@professores_bp.route("/", methods=["GET"])
def buscar_professores():
    professores = listar_professores()

    resultado = []

    for professor in professores:
        resultado.append({
            "id_professor": professor[0],
            "nome": professor[1],
            "cpf": professor[2],
            "email": professor[3],
            "formacao": professor[4],
            "carga_horaria_semanal": professor[5]
        })

    return jsonify(resultado)

@professores_bp.route("/<int:id_professor>", methods=["GET"])
def buscar_professor(id_professor):
    professor = buscar_professor_db(id_professor)

    if professor is None:
        return jsonify({"erro": "Professor não encontrado"}), 404

    return jsonify({
        "id_professor": professor[0],
        "nome": professor[1],
        "cpf": professor[2],
        "email": professor[3],
        "formacao": professor[4],
        "carga_horaria_semanal": professor[5]
    })

@professores_bp.route("/", methods=["POST"])
def criar_professor():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados do professor em JSON"}), 400

    campos = [
        "nome",
        "cpf",
        "email",
        "formacao",
        "carga_horaria_semanal"
    ]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    try:
        cadastrar_professor(
            dados["nome"],
            dados["cpf"],
            dados["email"],
            dados["formacao"],
            dados["carga_horaria_semanal"]
        )
    except Exception:
        return jsonify({"erro": "Não foi possível cadastrar o professor. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Professor cadastrado com sucesso"}), 201

@professores_bp.route("/<int:id_professor>", methods=["PUT"])
def atualizar_professor(id_professor):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados do professor em JSON"}), 400

    campos = ["nome", "cpf", "email", "formacao", "carga_horaria_semanal"]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    professor = buscar_professor_db(id_professor)

    if professor is None:
        return jsonify({"erro": "Professor não encontrado"}), 404

    try:
        editar_professor(
            id_professor,
            dados["nome"],
            dados["cpf"],
            dados["email"],
            dados["formacao"],
            dados["carga_horaria_semanal"]
        )
    except Exception:
        return jsonify({"erro": "Não foi possível atualizar o cadastro do professor. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Professor atualizado com sucesso"}), 200

@professores_bp.route("/<int:id_professor>", methods=["DELETE"])
def deletar_professor(id_professor):
    professor = buscar_professor_db(id_professor)

    if professor is None:
        return jsonify({"erro": "Professor não encontrado"}), 404

    try:
        deletar_professor_db(id_professor)
    except Exception:
        return jsonify({"erro": "Não foi possível excluir o cadastro do professor."}), 400

    return jsonify({"mensagem": "Professor excluído com sucesso"}), 200

