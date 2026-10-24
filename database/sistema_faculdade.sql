CREATE DATABASE IF NOT EXISTS sistema_faculdade;
USE sistema_faculdade;

CREATE TABLE CURSO (
    id_curso INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_curso VARCHAR(100) NOT NULL,
    carga_horaria INT NOT NULL,
    turno VARCHAR(20) NOT NULL
);

CREATE TABLE PROFESSOR (
    id_professor INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    formacao VARCHAR(50) NOT NULL,
    carga_horaria_semanal INT NOT NULL
);

CREATE TABLE CADALU (
    id_aluno INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    id_curso INT NOT NULL,
    CONSTRAINT fk_aluno_curso
        FOREIGN KEY (id_curso) REFERENCES CURSO(id_curso)
);

CREATE TABLE DISCIPLINA (
    id_disciplina INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_disciplina VARCHAR(100) NOT NULL,
    carga_horaria INT NOT NULL,
    id_curso INT NOT NULL,
    CONSTRAINT fk_disciplina_curso
        FOREIGN KEY (id_curso) REFERENCES CURSO(id_curso)
);

CREATE TABLE PROFESSOR_DISCIPLINA (
    id_professor INT NOT NULL,
    id_disciplina INT NOT NULL,
    carga_horaria INT NOT NULL,
    PRIMARY KEY (id_professor, id_disciplina),
    CONSTRAINT fk_professor_disciplina_professor
        FOREIGN KEY (id_professor) REFERENCES PROFESSOR(id_professor),
    CONSTRAINT fk_professor_disciplina_disciplina
        FOREIGN KEY (id_disciplina) REFERENCES DISCIPLINA(id_disciplina)
);

INSERT INTO CURSO (nome_curso, carga_horaria, turno) VALUES
('ADS', 2833, 'noite'),
('Engenharia civil', 3300, 'noite'),
('Microeletronica', 3200, 'manha'),
('Gestao de qualidade', 2880, 'noite');

INSERT INTO PROFESSOR
(nome, cpf, email, formacao, carga_horaria_semanal) VALUES
('Roberto', '11111111111', 'roberto@gmail.com', 'Mestre', 40),
('Joao', '22222222222', 'joao@gmail.com', 'Doutor', 80),
('Maria', '33333333333', 'maria@gmail.com', 'Mestre', 40),
('Pedro', '44444444444', 'pedro@gmail.com', 'Mestre', 80);

INSERT INTO CADALU
(nome, cpf, email, data_nascimento, id_curso) VALUES
('Henrique', '55555555555', 'henrique@gmail.com', '2001-01-01', 4),
('Gabriel', '66666666666', 'gabriel@gmail.com', '2006-06-06', 2),
('Guilherme', '77777777777', 'guilherme@gmail.com', '2003-09-09', 3),
('Paulo', '88888888888', 'paulo@gmail.com', '2002-07-07', 1);

INSERT INTO DISCIPLINA
(nome_disciplina, carga_horaria, id_curso) VALUES
('Metrologia e calibracao', 30, 4),
('Seguranca do trabalho', 50, 2),
('Laboratorio de banco de dados', 80, 1),
('Instrumentacao eletronica', 45, 3);

INSERT INTO PROFESSOR_DISCIPLINA
(id_professor, id_disciplina, carga_horaria) VALUES
(4, 1, 30),
(2, 2, 50),
(3, 3, 80),
(1, 4, 45);