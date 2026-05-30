# API Bancária Assíncrona com FastAPI

Este projeto é uma API RESTful desenvolvida para gerenciar contas bancárias simples, permitindo realizar saques, depósitos e emitir extratos de forma segura e totalmente assíncrona. O desenvolvimento foi feito com foco em boas práticas de design de API, validação estrita de dados e autenticação robusta.

## O que a API faz

*   **Cadastro e Login:** Sistema de criação de conta e login que gera tokens JWT para autenticar as requisições subsequentes.
*   **Depósitos:** Adiciona saldo à conta corrente cadastrada. Há uma validação que impede depósitos de valores zerados ou negativos.
*   **Saques:** Deduz o valor do saldo da conta corrente após verificar se o usuário possui saldo suficiente e se o valor solicitado é válido (maior que zero).
*   **Extrato consolidado:** Retorna o saldo atual atualizado e lista todas as movimentações (depósitos e saques) associadas à conta.

## Tecnologias utilizadas

*   **FastAPI:** Framework moderno e rápido para construção de APIs em Python, aproveitando recursos assíncronos (`async/await`) para lidar com I/O de maneira eficiente.
*   **SQLAlchemy 2.0 & aiosqlite:** ORM configurado em modo assíncrono para interagir com o banco de dados local SQLite sem bloquear a execução da aplicação.
*   **Pydantic v2:** Utilizado para validar a estrutura dos payloads das requisições e formatar as respostas JSON retornadas ao cliente (com suporte a fusos horários via `AwareDatetime`).
*   **PyJWT & Passlib:** Ferramentas essenciais para a segurança, lidando com a decodificação dos tokens JWT e hashing seguro das senhas (utilizando bcrypt).

## Estrutura do Código

A aplicação está organizada de forma modular:

*   `app/core/`: Configurações de ambiente (`config.py`) e lógica de criptografia/JWT (`security.py`).
*   `app/db/`: Inicialização da conexão assíncrona do banco (`database.py`) e os modelos de dados do SQLAlchemy para contas e transações (`models.py`).
*   `app/schemas/`: Schemas Pydantic que garantem a tipagem e validação dos dados de entrada e saída.
*   `app/api/`: Rotas (/auth, /transactions, /account) e as injeções de dependências como a de validação de token do usuário.
*   `app/main.py`: Arquivo principal que configura e inicializa o servidor FastAPI e o banco de dados.

## Como rodar o projeto

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd <pasta-do-projeto>
    ```

2.  **Crie e ative o ambiente virtual:**
    *   No Windows:
        ```powershell
        py -m venv venv
        .\venv\Scripts\Activate.ps1
        ```
    *   No Linux/macOS:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie as variáveis de ambiente:**
    Copie ou renomeie o arquivo `.env` na raiz do projeto e configure a chave de assinatura dos tokens e a URL do banco (caso queira alterar):
    ```env
    SECRET_KEY=sua_chave_secreta_super_segura
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=sqlite+aiosqlite:///./bank.db
    ```

5.  **Inicie a aplicação:**
    ```bash
    python -m uvicorn app.main:app --reload
    ```

6.  **Acesse a documentação interativa:**
    Com o servidor rodando, abra o navegador em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para realizar chamadas de teste, cadastrar usuários, fazer login e simular as transações diretamente pela interface do Swagger.
