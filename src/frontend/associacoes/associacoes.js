const API = "http://127.0.0.1:5000/api/associacoes";

const lista = document.getElementById("listaAssociacoes");
const formAssociacao = document.getElementById("formAssociacao");


async function listarAssociacoes() {
    try {
        const resposta = await fetch(`${API}/`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar associações");
        }

        const associacoes = await resposta.json();
        lista.innerHTML = "";

        associacoes.forEach(associacao => {
            const item = document.createElement("li");

            item.textContent =
                `Professor ${associacao.id_professor} - ` +
                `Disciplina ${associacao.id_disciplina} - ` +
                `Carga horária: ${associacao.carga_horaria} `;

            const botaoExcluir = document.createElement("button");
            botaoExcluir.textContent = "Excluir";

            botaoExcluir.addEventListener("click", async () => {
                if (!confirm("Deseja excluir esta associação?")) {
                    return;
                }

                try {
                    const resposta = await fetch(
                        `${API}/${associacao.id_professor}/${associacao.id_disciplina}`,
                        { method: "DELETE" }
                    );

                    const resultado = await resposta.json();

                    if (!resposta.ok) {
                        alert(resultado.erro || "Não foi possível excluir.");
                        return;
                    }

                    alert("Associação excluída com sucesso!");
                    listarAssociacoes();

                } catch (erro) {
                    alert("Erro ao conectar com a API.");
                    console.error(erro);
                }
            });

            item.appendChild(botaoExcluir);
            lista.appendChild(item);
        });

    } catch (erro) {
        alert("Não foi possível carregar as associações.");
        console.error(erro);
    }
}

document.getElementById("btnListar")
    .addEventListener("click", listarAssociacoes);

formAssociacao.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const associacao = {
        id_professor: Number(document.getElementById("idProfessor").value),
        id_disciplina: Number(document.getElementById("idDisciplina").value),
        carga_horaria: Number(document.getElementById("cargaHoraria").value)
    };

    try {
        const resposta = await fetch(`${API}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(associacao)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert(resultado.erro || "Erro ao cadastrar associação.");
            return;
        }

        alert("Associação cadastrada com sucesso!");
        formAssociacao.reset();
        listarAssociacoes();

    } catch (erro) {
        alert("Não foi possível conectar à API.");
        console.error(erro);
    }
});


document.getElementById("btnBuscar")
    .addEventListener("click", async () => {
        const idProfessor =
            document.getElementById("idProfessorBusca").value;

        const idDisciplina =
            document.getElementById("idDisciplinaBusca").value;

        const resultado = document.getElementById("resultadoBusca");

        if (!idProfessor || !idDisciplina) {
            alert("Informe o ID do professor e o ID da disciplina.");
            return;
        }

        try {
            const resposta = await fetch(
                `${API}/${idProfessor}/${idDisciplina}`
            );

            const associacao = await resposta.json();

            if (!resposta.ok) {
                resultado.textContent =
                    associacao.erro || "Associação não encontrada.";
                return;
            }

            resultado.textContent =
                `Professor: ${associacao.id_professor} | ` +
                `Disciplina: ${associacao.id_disciplina} | ` +
                `Carga horária: ${associacao.carga_horaria}`;

            document.getElementById("editarIdProfessor").value =
                associacao.id_professor;

            document.getElementById("editarIdDisciplina").value =
                associacao.id_disciplina;

            document.getElementById("editarCargaHoraria").value =
                associacao.carga_horaria;

        } catch (erro) {
            alert("Erro ao buscar associação.");
            console.error(erro);
        }
    });

document.getElementById("formEditar")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const idProfessor =
            document.getElementById("editarIdProfessor").value;

        const idDisciplina =
            document.getElementById("editarIdDisciplina").value;

        const associacao = {
            carga_horaria: Number(
                document.getElementById("editarCargaHoraria").value
            )
        };

        try {
            const resposta = await fetch(
                `${API}/${idProfessor}/${idDisciplina}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(associacao)
                }
            );

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível editar a associação.");
                return;
            }

            alert("Associação atualizada com sucesso!");
            listarAssociacoes();

        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });