const API = "http://127.0.0.1:5000/api/alunos";

const lista = document.getElementById("listaAlunos");
const formAluno = document.getElementById("formAluno");

async function listarAlunos() {
    try {
        const resposta = await fetch(`${API}/`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar alunos");
        }

        const alunos = await resposta.json();

        lista.innerHTML = "";

        alunos.forEach(aluno => {
            const item = document.createElement("li");

            item.textContent = `${aluno.id_aluno} - ${aluno.nome} `;

            const botaoExcluir = document.createElement("button");
            botaoExcluir.textContent = "Excluir";

            botaoExcluir.addEventListener("click", async () => {
                if (!confirm(`Deseja excluir o aluno ${aluno.nome}?`)) {
                    return;
                }

                try {
                    const resposta = await fetch(
                        `${API}/${aluno.id_aluno}`,
                        { method: "DELETE" }
                    );

                    const resultado = await resposta.json();

                    if (!resposta.ok) {
                        alert(resultado.erro || "Não foi possível excluir.");
                        return;
                    }

                    alert("Aluno excluído com sucesso!");
                    listarAlunos();
                } catch (erro) {
                    alert("Erro ao conectar com a API.");
                    console.error(erro);
                }
            });

            item.appendChild(botaoExcluir);
            lista.appendChild(item);
        });
    } catch (erro) {
        alert("Não foi possível carregar os alunos.");
        console.error(erro);
    }
}

document.getElementById("btnListar")
    .addEventListener("click", listarAlunos);


formAluno.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const aluno = {
        nome: document.getElementById("nome").value,
        cpf: document.getElementById("cpf").value,
        email: document.getElementById("email").value,
        data_nascimento: document.getElementById("dataNascimento").value,
        id_curso: Number(document.getElementById("idCurso").value)
    };

    try {
        const resposta = await fetch(`${API}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(aluno)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert(resultado.erro || "Erro ao cadastrar aluno.");
            return;
        }

        alert("Aluno cadastrado com sucesso!");
        formAluno.reset();
        listarAlunos();
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
            alert("Digite o ID do aluno.");
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`);
            const aluno = await resposta.json();

            if (!resposta.ok) {
                resultado.textContent =
                    aluno.erro || "Aluno não encontrado.";
                return;
            }

            resultado.textContent =
                `ID: ${aluno.id_aluno} | Nome: ${aluno.nome} | CPF: ${aluno.cpf} | E-mail: ${aluno.email}`;

            // Preenche o formulário de edição
            document.getElementById("editarId").value = aluno.id_aluno;
            document.getElementById("editarNome").value = aluno.nome;
            document.getElementById("editarCpf").value = aluno.cpf;
            document.getElementById("editarEmail").value = aluno.email;
            document.getElementById("editarDataNascimento").value =
                String(aluno.data_nascimento).substring(0, 10);
            document.getElementById("editarIdCurso").value = aluno.id_curso;

        } catch (erro) {
            alert("Erro ao buscar aluno.");
            console.error(erro);
        }
    });

document.getElementById("formEditar")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("editarId").value;

        const aluno = {
            nome: document.getElementById("editarNome").value,
            cpf: document.getElementById("editarCpf").value,
            email: document.getElementById("editarEmail").value,
            data_nascimento: document.getElementById("editarDataNascimento").value,
            id_curso: Number(document.getElementById("editarIdCurso").value)
        };

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(aluno)
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível editar o aluno.");
                return;
            }

            alert("Aluno atualizado com sucesso!");
            listarAlunos();
        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });

document.getElementById("formExcluirAluno")
    .addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const id = document.getElementById("excluirIdAluno").value;

        if (!confirm(`Deseja excluir o aluno de ID ${id}?`)) {
            return;
        }

        try {
            const resposta = await fetch(`${API}/${id}`, {
                method: "DELETE"
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                alert(resultado.erro || "Não foi possível excluir o aluno.");
                return;
            }

            alert("Aluno excluído com sucesso!");
            document.getElementById("formExcluirAluno").reset();
            document.getElementById("resultadoBusca").textContent = "";
            listarAlunos();
        } catch (erro) {
            alert("Erro ao conectar com a API.");
            console.error(erro);
        }
    });