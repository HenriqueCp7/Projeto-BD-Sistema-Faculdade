from flask import Blueprint, jsonify, request
from ..database import listar_cursos, buscar_curso as buscar_curso_db, cadastrar_curso, editar_curso, deletar_curso as deletar_curso_db

cursos_bp = Blueprint("cursos", __name__, url_prefix="/api/cursos")


@cursos_bp.route("/", methods=["GET"])
def buscar_cursos():
    cursos = listar_cursos()

    resultado = []

    for curso in cursos:
        resultado.append({
            "id_curso": curso[0],
            "nome_curso": curso[1],
            "carga_horaria": curso[2],
            "turno": curso[3]
        })

    return jsonify(resultado)

@cursos_bp.route("/<int:id_curso>", methods=["GET"])
def buscar_curso(id_curso):
    curso = buscar_curso_db(id_curso)

    if curso is None:
        return jsonify({"erro": "Curso não encontrado"}), 404

    return jsonify({
        "id_curso": curso[0],
        "nome_curso": curso[1],
        "carga_horaria": curso[2],
        "turno": curso[3]
    })

@cursos_bp.route("/", methods=["POST"])
def criar_curso():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados do curso em JSON"}), 400

    campos = [
        "nome_curso",
        "carga_horaria",
        "turno",
    ]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    try:
        cadastrar_curso(
            dados["nome_curso"],
            dados["carga_horaria"],
            dados["turno"],
        )
    except Exception:
        return jsonify({"erro": "Não foi possível cadastrar o curso. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Curso cadastrado com sucesso"}), 201

@cursos_bp.route("/<int:id_curso>", methods=["PUT"])
def atualizar_curso(id_curso):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados do curso em JSON"}), 400

    campos = ["nome_curso", "carga_horaria", "turno"]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    curso = buscar_curso_db(id_curso)

    if curso is None:
        return jsonify({"erro": "Curso não encontrado"}), 404

    try:
        editar_curso(
            id_curso,
            dados["nome_curso"],
            dados["carga_horaria"],
            dados["turno"],
        )
    except Exception:
        return jsonify({"erro": "Não foi possível atualizar o curso. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Curso atualizado com sucesso"}), 200

@cursos_bp.route("/<int:id_curso>", methods=["DELETE"])
def deletar_curso(id_curso):
    curso = buscar_curso_db(id_curso)

    if curso is None:
        return jsonify({"erro": "Curso não encontrado"}), 404

    try:
        deletar_curso_db(id_curso)
    except Exception:
        return jsonify({"erro": "Não foi possível excluir o curso."}), 400

    return jsonify({"mensagem": "Curso excluído com sucesso"}), 200

