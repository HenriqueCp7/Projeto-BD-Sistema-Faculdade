from flask import Flask
from flask_cors import CORS
from .routes.alunos import alunos_bp
from .routes.cursos import cursos_bp
from .routes.professores import professores_bp
from .routes.disciplinas import disciplinas_bp
from .routes.associacoes import associacoes_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(alunos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(associacoes_bp)

if __name__ == "__main__":
    app.run(debug=True)