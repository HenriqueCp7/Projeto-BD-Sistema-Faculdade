const API = "http://127.0.0.1:5000/api/cursos";

const lista = document.getElementById("listaCursos");
const formCurso = document.getElementById("formCurso");

async function listarCursos() {
    try {
        const resposta = await fetch(`${API}/`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar cursos");
        }

        const cursos = await resposta.json();
        lista.innerHTML = "";

        cursos.forEach(curso => {
            const item = document.createElement("li");

            item.textContent =
                `${curso.id_curso} - ${curso.nome_curso} `;

            const botaoExcluir = document.createElement("button");
            botaoExcluir.textContent = "Excluir";

            botaoExcluir.addEventListener("click", async () => {
                if (!confirm(`Deseja excluir o curso ${curso.nome_curso}?`)) {
                    return;
                }

                try {
                    const resposta = await fetch(
                        `${API}/${curso.id_curso}`,
                        { method: "DELETE" }
                    );

                    const resultado = await resposta.json();

                    if (!resposta.ok) {
                        alert(resultado.erro || "Não foi possível excluir o curso.");
                        return;
                    }

                    alert("Curso excluído com sucesso!");
                    listarCursos();

                } catch (erro) {
                    alert("Erro ao conectar com a API.");
                    console.error(erro);
                }
            });

            item.appendChild(botaoExcluir);
            lista.appendChild(item);
        });

    } catch (erro) {
        alert("Não foi possível carregar os cursos.");
        console.error(erro);
    }
}

document.getElementById("btnListar")
    .addEventListener("click", listarCursos);


formCurso.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const curso = {
        nome_curso: document.getElementById("nomeCurso").value,
        carga_horaria: Number(document.getElementById("cargaHoraria").value),
        turno: document.getElementById("turno").value
    };

    try {
        const resposta = await fetch(`${API}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(curso)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert(resultado.erro || "Erro ao cadastrar curso.");
            return;
        }

        alert("Curso cadastrado com sucesso!");
        formCurso.reset();
        listarCursos();

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
            alert("Digite o ID do curso.");
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`);
            const curso = await resposta.json();

            if (!resposta.ok) {
                resultado.textContent =
                    curso.erro || "Curso não encontrado.";
                return;
            }

            resultado.textContent =
                `ID: ${curso.id_curso} | Nome: ${curso.nome_curso} | Carga horária: ${curso.carga_horaria} | Turno: ${curso.turno}`;

            document.getElementById("editarId").value = curso.id_curso;
            document.getElementById("editarNome").value = curso.nome_curso;
            document.getElementById("editarCargaHoraria").value = curso.carga_horaria;
            document.getElementById("editarTurno").value = curso.turno;

        } catch (erro) {
            alert("Erro ao buscar curso.");
            console.error(erro);
        }
    });


document.getElementById("formEditar")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("editarId").value;

        const curso = {
            nome_curso: document.getElementById("editarNome").value,
            carga_horaria: Number(document.getElementById("editarCargaHoraria").value),
            turno: document.getElementById("editarTurno").value
        };

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(curso)
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível editar o curso.");
                return;
            }

            alert("Curso atualizado com sucesso!");
            listarCursos();

        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });

document.getElementById("formExcluirCurso")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("excluirIdCurso").value;

        if (!confirm(`Deseja excluir o curso de ID ${id}?`)) {
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "DELETE"
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível excluir o curso.");
                return;
            }

            alert("Curso excluído com sucesso!");
            document.getElementById("formExcluirCurso").reset();
            document.getElementById("resultadoBusca").textContent = "";
            listarCursos();
        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });