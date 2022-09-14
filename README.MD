# Projeto AdoPT 🐶🐱 Back-end

Adopt é um sistema de adoção de animais, voltado para instituições sem fins lucrativos.  
O projeto constitui de uma vitrine de animais capaz de divulgar e gerenciar os animais disponiveis para adoção, além de um sistema de cadastro de usuários.

## Recursos

- [ ] Área Administrativa
- [ ] Vitrine de animais
- [ ] Cadastro de animais
- [ ] Cadastro de usuários
- [ ] Solicitação de adoção
- [ ] Notificação de adoção

## 🚀 Rodando o projeto

Essas instruções permitirão que você obtenha uma copia do projeto em sua maquina local com proposito de desenvolvimento ou testes.

## 📋 Pre-requisitos

[Python versão 3.9](https://www.python.org/downloads/)


## 🔧 Instalação e Execução

Instruções de como instalar e rodar o projeto em um ambiente local.

1. Clone o projeto
```
git clone https://github.com/Ruy-Araujo/adopt-backend.git
cd adopt-backend
```

2. Instale as dependencias necessarias
```console
pip install -r requirements.txt
```

3. Altere o arquivo exemple.env para .env e adiciona as variaveis de ambiente 

3.1 Para gerar uma SECRET_KEY, use o comando
```console
openssl rand -hex 32
```

Rode o projeto
```console
uvicorn main:app --reload
```

Após isso o projeto estará rodando no endereço local: http://127.0.0.1:8000

## 🛠️ Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)

## Autores

[<img src="https://avatars.githubusercontent.com/u/53796141?v=4" width="80px" style="border-radius:50%"/>](https://github.com/Ruy-Araujo)

_Ruy Araujo_

[<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/ruy-araujo/)
[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>](https://github.com/Ruy-Araujo)

[<img src="https://avatars.githubusercontent.com/u/32309203?v=4" width="80px" style="border-radius:50%"/>](https://github.com/caiobas)

_caiobas_

[<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>]()
[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>](https://github.com/caiobas)

[<img src="https://avatars.githubusercontent.com/u/90728045?v=4" width="80px" style="border-radius:50%"/>](https://github.com/CamillaTB)

_CamillaTB_

[<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>]()
[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>](https://github.com/CamillaTB)

## 📄 License

[MIT license](https://github.com/Ruy-Araujo/adopt-backend/blob/master/LICENSE)
