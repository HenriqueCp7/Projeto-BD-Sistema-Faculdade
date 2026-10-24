const API = "http://127.0.0.1:5000/api/disciplinas";

const lista = document.getElementById("listaDisciplinas");
const formDisciplina = document.getElementById("formDisciplina");

async function listarDisciplinas() {
    try {
        const resposta = await fetch(`${API}/`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar disciplinas");
        }

        const disciplinas = await resposta.json();
        lista.innerHTML = "";

        disciplinas.forEach(disciplina => {
            const item = document.createElement("li");

            item.textContent =
                `${disciplina.id_disciplina} - ${disciplina.nome_disciplina}`;

            const botaoExcluir = document.createElement("button");
            botaoExcluir.textContent = "Excluir";

            botaoExcluir.addEventListener("click", async () => {
                if (!confirm(
                    `Deseja excluir a disciplina ${disciplina.nome_disciplina}?`
                )) {
                    return;
                }

                try {
                    const resposta = await fetch(
                        `${API}/${disciplina.id_disciplina}`,
                        { method: "DELETE" }
                    );

                    const resultado = await resposta.json();

                    if (!resposta.ok) {
                        alert(resultado.erro || "Não foi possível excluir.");
                        return;
                    }

                    alert("Disciplina excluída com sucesso!");
                    listarDisciplinas();

                } catch (erro) {
                    alert("Erro ao conectar com a API.");
                    console.error(erro);
                }
            });

            item.appendChild(botaoExcluir);
            lista.appendChild(item);
        });

    } catch (erro) {
        alert("Não foi possível carregar as disciplinas.");
        console.error(erro);
    }
}

document.getElementById("btnListar")
    .addEventListener("click", listarDisciplinas);


formDisciplina.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const disciplina = {
        nome_disciplina: document.getElementById("nomeDisciplina").value,
        carga_horaria: Number(
            document.getElementById("cargaHoraria").value
        ),
        id_curso: Number(document.getElementById("idCurso").value)
    };

    try {
        const resposta = await fetch(`${API}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(disciplina)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert(resultado.erro || "Erro ao cadastrar disciplina.");
            return;
        }

        alert("Disciplina cadastrada com sucesso!");
        formDisciplina.reset();
        listarDisciplinas();

    } catch (erro) {
        alert("Não foi possível conectar à API.");
        console.error(erro);
    }
});

document.getElementById("btnBuscar")
    .addEventListener("click", async () => {
        const id = document.getElementById("idBusca").value;
        const resultado = document.getElementById("resultadoBusca");

        if (!id) {
            alert("Digite o ID da disciplina.");
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`);
            const disciplina = await resposta.json();

            if (!resposta.ok) {
                resultado.textContent =
                    disciplina.erro || "Disciplina não encontrada.";
                return;
            }

            resultado.textContent =
                `ID: ${disciplina.id_disciplina} | Nome: ${disciplina.nome_disciplina} | Carga horária: ${disciplina.carga_horaria} | Curso: ${disciplina.id_curso}`;

            document.getElementById("editarId").value =
                disciplina.id_disciplina;

            document.getElementById("editarNome").value =
                disciplina.nome_disciplina;

            document.getElementById("editarCargaHoraria").value =
                disciplina.carga_horaria;

            document.getElementById("editarIdCurso").value =
                disciplina.id_curso;

        } catch (erro) {
            alert("Erro ao buscar disciplina.");
            console.error(erro);
        }
    });

document.getElementById("formEditar")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("editarId").value;

        const disciplina = {
            nome_disciplina: document.getElementById("editarNome").value,
            carga_horaria: Number(
                document.getElementById("editarCargaHoraria").value
            ),
            id_curso: Number(
                document.getElementById("editarIdCurso").value
            )
        };

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(disciplina)
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível editar a disciplina.");
                return;
            }

            alert("Disciplina atualizada com sucesso!");
            listarDisciplinas();

        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });

document.getElementById("formExcluirDisciplina")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("excluirIdDisciplina").value;

        if (!confirm(`Deseja excluir a disciplina de ID ${id}?`)) {
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "DELETE"
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível excluir a disciplina.");
                return;
            }

            alert("Disciplina excluída com sucesso!");
            document.getElementById("formExcluirDisciplina").reset();
            document.getElementById("resultadoBusca").textContent = "";
            listarDisciplinas();
        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });