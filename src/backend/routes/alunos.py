
from flask import Blueprint, jsonify, request
from ..database import listar_alunos, buscar_aluno as buscar_aluno_db, cadastrar_aluno, editar_aluno, deletar_aluno as deletar_aluno_db

alunos_bp = Blueprint("alunos", __name__, url_prefix="/api/alunos")


@alunos_bp.route("/", methods=["GET"])
def buscar_alunos():
    alunos = listar_alunos()

    resultado = []

    for aluno in alunos:
        resultado.append({
            "id_aluno": aluno[0],
            "nome": aluno[1],
            "cpf": aluno[2],
            "email": aluno[3],
            "data_nascimento": aluno[4],
            "id_curso": aluno[5],
            "nome_curso": aluno[6]
        })

    return jsonify(resultado)

@alunos_bp.route("/<int:id_aluno>", methods=["GET"])
def buscar_aluno(id_aluno):
    aluno = buscar_aluno_db(id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify({
        "id_aluno": aluno[0],
        "nome": aluno[1],
        "cpf": aluno[2],
        "email": aluno[3],
        "data_nascimento": str(aluno[4]),
        "id_curso": aluno[5],
        "nome_curso": aluno[6]
    })

@alunos_bp.route("/", methods=["POST"])
def criar_aluno():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados do aluno em JSON"}), 400

    campos = [
        "nome",
        "cpf",
        "email",
        "data_nascimento",
        "id_curso",
    ]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    try:
        cadastrar_aluno(
            dados["nome"],
            dados["cpf"],
            dados["email"],
            dados["data_nascimento"],
            dados["id_curso"]
        )
    except Exception:
        return jsonify({"erro": "Não foi possível cadastrar o aluno. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Aluno cadastrado com sucesso"}), 201

@alunos_bp.route("/<int:id_aluno>", methods=["PUT"])
def atualizar_aluno(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados do aluno em JSON"}), 400

    campos = ["nome", "cpf", "email", "data_nascimento", "id_curso"]

    if any(campo not in dados for campo in campos):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    aluno = buscar_aluno_db(id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    try:
        editar_aluno(
            id_aluno,
            dados["nome"],
            dados["cpf"],
            dados["email"],
            dados["data_nascimento"],
            dados["id_curso"]
        )
    except Exception as e:
        print(f"Erro ao atualizar aluno: {e}")
        return jsonify({"erro": "Não foi possível atualizar o aluno. Verifique os dados enviados."}), 400

    return jsonify({"mensagem": "Aluno atualizado com sucesso"}), 200

@alunos_bp.route("/<int:id_aluno>", methods=["DELETE"])
def deletar_aluno(id_aluno):
    aluno = buscar_aluno_db(id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    try:
        deletar_aluno_db(id_aluno)
    except Exception:
        return jsonify({"erro": "Não foi possível excluir o aluno."}), 400

    return jsonify({"mensagem": "Aluno excluído com sucesso"}), 200

