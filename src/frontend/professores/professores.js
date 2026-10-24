const API = "http://127.0.0.1:5000/api/professores";

const lista = document.getElementById("listaProfessores");
const formProfessor = document.getElementById("formProfessor");

async function listarProfessores() {
    try {
        const resposta = await fetch(`${API}/`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar professores");
        }

        const professores = await resposta.json();
        lista.innerHTML = "";

        professores.forEach(professor => {
            const item = document.createElement("li");

            item.textContent =
                `${professor.id_professor} - ${professor.nome}`;

            const botaoExcluir = document.createElement("button");
            botaoExcluir.textContent = "Excluir";

            botaoExcluir.addEventListener("click", async () => {
                if (!confirm(`Deseja excluir o professor ${professor.nome}?`)) {
                    return;
                }

                try {
                    const resposta = await fetch(
                        `${API}/${professor.id_professor}`,
                        { method: "DELETE" }
                    );

                    const resultado = await resposta.json();

                    if (!resposta.ok) {
                        alert(resultado.erro || "Não foi possível excluir.");
                        return;
                    }

                    alert("Professor excluído com sucesso!");
                    listarProfessores();

                } catch (erro) {
                    alert("Erro ao conectar com a API.");
                    console.error(erro);
                }
            });

            item.appendChild(botaoExcluir);
            lista.appendChild(item);
        });

    } catch (erro) {
        alert("Não foi possível carregar os professores.");
        console.error(erro);
    }
}

document.getElementById("btnListar")
    .addEventListener("click", listarProfessores);


formProfessor.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const professor = {
        nome: document.getElementById("nome").value,
        cpf: document.getElementById("cpf").value,
        email: document.getElementById("email").value,
        formacao: document.getElementById("formacao").value,
        carga_horaria_semanal: Number(
            document.getElementById("cargaHoraria").value
        )
    };

    try {
        const resposta = await fetch(`${API}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(professor)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert(resultado.erro || "Erro ao cadastrar professor.");
            return;
        }

        alert("Professor cadastrado com sucesso!");
        formProfessor.reset();
        listarProfessores();

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
            alert("Digite o ID do professor.");
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`);
            const professor = await resposta.json();

            if (!resposta.ok) {
                resultado.textContent =
                    professor.erro || "Professor não encontrado.";
                return;
            }

            resultado.textContent =
                `ID: ${professor.id_professor} | Nome: ${professor.nome} | CPF: ${professor.cpf} | E-mail: ${professor.email} | Formação: ${professor.formacao} | Carga horária semanal: ${professor.carga_horaria_semanal}`;

            document.getElementById("editarId").value =
                professor.id_professor;

            document.getElementById("editarNome").value =
                professor.nome;

            document.getElementById("editarCpf").value =
                professor.cpf;

            document.getElementById("editarEmail").value =
                professor.email;

            document.getElementById("editarFormacao").value =
                professor.formacao;

            document.getElementById("editarCargaHoraria").value =
                professor.carga_horaria_semanal;

        } catch (erro) {
            alert("Erro ao buscar professor.");
            console.error(erro);
        }
    });


document.getElementById("formEditar")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("editarId").value;

        const professor = {
            nome: document.getElementById("editarNome").value,
            cpf: document.getElementById("editarCpf").value,
            email: document.getElementById("editarEmail").value,
            formacao: document.getElementById("editarFormacao").value,
            carga_horaria_semanal: Number(
                document.getElementById("editarCargaHoraria").value
            )
        };

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(professor)
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível editar o professor.");
                return;
            }

            alert("Professor atualizado com sucesso!");
            listarProfessores();

        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });

document.getElementById("formExcluirProfessor")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("excluirIdProfessor").value;

        if (!confirm(`Deseja excluir o professor de ID ${id}?`)) {
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "DELETE"
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível excluir o professor.");
                return;
            }

            alert("Professor excluído com sucesso!");
            document.getElementById("formExcluirProfessor").reset();
            document.getElementById("resultadoBusca").textContent = "";
            listarProfessores();
        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });