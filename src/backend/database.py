import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="sistema_faculdade"
    )

    return conexao

#CRUD ALUNOS
def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            aluno.id_aluno,
            aluno.nome,
            aluno.cpf,
            aluno.email,
            aluno.data_nascimento,
            aluno.id_curso,
            curso.nome_curso
        FROM CADALU aluno
        INNER JOIN CURSO curso
            ON aluno.id_curso = curso.id_curso
    """)

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()
    return alunos

def buscar_aluno(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            aluno.id_aluno,
            aluno.nome,
            aluno.cpf,
            aluno.email,
            aluno.data_nascimento,
            aluno.id_curso,
            curso.nome_curso
        FROM CADALU aluno
        INNER JOIN CURSO curso
            ON aluno.id_curso = curso.id_curso
        WHERE aluno.id_aluno = %s
    """, (id_aluno,))

    aluno = cursor.fetchone()

    cursor.close()
    conexao.close()

    return aluno

def cadastrar_aluno(nome, cpf, email, data_nascimento, id_curso):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO CADALU
            (nome, cpf, email, data_nascimento, id_curso)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (nome, cpf, email, data_nascimento, id_curso)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def editar_aluno(id_aluno, nome, cpf, email, data_nascimento, id_curso):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE CADALU
        SET nome = %s,
            cpf = %s,
            email = %s,
            data_nascimento = %s,
            id_curso = %s
        WHERE id_aluno = %s
    """

    valores = (
        nome, cpf, email, data_nascimento, id_curso, id_aluno
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def deletar_aluno(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM CADALU WHERE id_aluno = %s"

    cursor.execute(sql, (id_aluno,))
    conexao.commit()

    cursor.close()
    conexao.close()

#CRUD CURSOS
def listar_cursos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_curso, nome_curso, carga_horaria, turno
        FROM CURSO
        ORDER BY nome_curso
    """)

    cursos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return cursos

def buscar_curso(id_curso):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_curso,
            nome_curso,
            carga_horaria,
            turno
        FROM CURSO
        WHERE id_curso = %s
    """, (id_curso,))

    curso = cursor.fetchone()
    
    cursor.close()
    conexao.close()

    return curso

def cadastrar_curso(nome_curso, carga_horaria, turno):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO CURSO
            (nome_curso, carga_horaria, turno) 
        VALUES (%s, %s, %s)
    """

    valores = (nome_curso, carga_horaria, turno)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def editar_curso(id_curso, nome_curso, carga_horaria, turno):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE CURSO
        SET nome_curso = %s,
            carga_horaria = %s,
            turno = %s
        WHERE id_curso = %s
    """

    valores = (nome_curso, carga_horaria, turno, id_curso)

    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()

def deletar_curso(id_curso):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM CURSO WHERE id_curso = %s"

    cursor.execute(sql, (id_curso,))
    conexao.commit()

    cursor.close()
    conexao.close()

#CRUD PROFESSORES
def listar_professores():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_professor,
            nome,
            cpf,
            email,
            formacao,
            carga_horaria_semanal
        FROM PROFESSOR
        ORDER BY nome
    """)

    professor = cursor.fetchall()

    cursor.close()
    conexao.close()
    return professor

def buscar_professor(id_professor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_professor,
            nome,
            cpf,
            email,
            formacao,
            carga_horaria_semanal
        FROM PROFESSOR
        WHERE id_professor = %s
    """, (id_professor,))

    professor = cursor.fetchone()

    cursor.close()
    conexao.close()

    return professor

def cadastrar_professor(nome, cpf, email, formacao, carga_horaria_semanal):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO PROFESSOR
            (nome, cpf, email, formacao, carga_horaria_semanal) 
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (nome, cpf, email, formacao, carga_horaria_semanal)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def editar_professor(id_professor, nome, cpf, email, formacao, carga_horaria_semanal):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE PROFESSOR
        SET nome = %s,
            cpf = %s,
            email = %s,
            formacao = %s,
            carga_horaria_semanal = %s
        WHERE id_professor = %s
    """

    valores = (nome, cpf, email, formacao, carga_horaria_semanal, id_professor)

    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()

def deletar_professor(id_professor):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM PROFESSOR WHERE id_professor = %s"

    cursor.execute(sql, (id_professor,))
    conexao.commit()

    cursor.close()
    conexao.close()

#CRUD DISCIPLINAS
def listar_disciplinas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            disciplina.id_disciplina,
            disciplina.nome_disciplina,
            disciplina.carga_horaria,
            disciplina.id_curso,
            curso.nome_curso
        FROM DISCIPLINA disciplina
        INNER JOIN CURSO curso
            ON disciplina.id_curso = curso.id_curso
        ORDER BY disciplina.nome_disciplina
    """)

    disciplina = cursor.fetchall()

    cursor.close()
    conexao.close()
    return disciplina

def buscar_disciplina(id_disciplina):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            disciplina.id_disciplina,
            disciplina.nome_disciplina,
            disciplina.carga_horaria,
            disciplina.id_curso,
            curso.nome_curso
        FROM DISCIPLINA disciplina
        INNER JOIN CURSO curso
            ON disciplina.id_curso = curso.id_curso
        WHERE disciplina.id_disciplina = %s
    """, (id_disciplina,))

    disciplina = cursor.fetchone()

    cursor.close()
    conexao.close()
    return disciplina

def cadastrar_disciplina(nome_disciplina, carga_horaria, id_curso):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO DISCIPLINA
            (nome_disciplina, carga_horaria, id_curso)
        VALUES (%s, %s, %s)
    """

    valores = (nome_disciplina, carga_horaria, id_curso)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def editar_disciplina(id_disciplina, nome_disciplina, carga_horaria, id_curso):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE DISCIPLINA
        SET nome_disciplina = %s,
            carga_horaria = %s,
            id_curso = %s
        WHERE id_disciplina = %s
    """

    valores = (nome_disciplina, carga_horaria, id_curso, id_disciplina)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def deletar_disciplina(id_disciplina):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM DISCIPLINA WHERE id_disciplina = %s"

    cursor.execute(sql, (id_disciplina,))
    conexao.commit()

    cursor.close()
    conexao.close()

#CRUD ASSOCIACOES
def listar_associacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pd.id_professor,
            professor.nome,
            pd.id_disciplina,
            disciplina.nome_disciplina,
            pd.carga_horaria
        FROM PROFESSOR_DISCIPLINA pd
        INNER JOIN PROFESSOR professor
            ON pd.id_professor = professor.id_professor
        INNER JOIN DISCIPLINA disciplina
            ON pd.id_disciplina = disciplina.id_disciplina
        ORDER BY professor.nome, disciplina.nome_disciplina
    """)

    associacoes = cursor.fetchall()
    cursor.close()
    conexao.close()

    return associacoes

def buscar_associacao(id_professor, id_disciplina):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_professor, id_disciplina, carga_horaria
        FROM PROFESSOR_DISCIPLINA
        WHERE id_professor = %s AND id_disciplina = %s
    """, (id_professor, id_disciplina))

    associacao = cursor.fetchone()
    cursor.close()
    conexao.close()

    return associacao

def cadastrar_associacao(id_professor, id_disciplina, carga_horaria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO PROFESSOR_DISCIPLINA
            (id_professor, id_disciplina, carga_horaria)
        VALUES (%s, %s, %s)
    """, (id_professor, id_disciplina, carga_horaria))

    conexao.commit()
    cursor.close()
    conexao.close()

def editar_associacao(id_professor, id_disciplina, carga_horaria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE PROFESSOR_DISCIPLINA
        SET carga_horaria = %s
        WHERE id_professor = %s AND id_disciplina = %s
    """, (carga_horaria, id_professor, id_disciplina))

    conexao.commit()
    cursor.close()
    conexao.close()

def deletar_associacao(id_professor, id_disciplina):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM PROFESSOR_DISCIPLINA
        WHERE id_professor = %s AND id_disciplina = %s
    """, (id_professor, id_disciplina))

    conexao.commit()
    cursor.close()
    conexao.close()