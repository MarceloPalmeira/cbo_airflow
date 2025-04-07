
## Pré-requisitos

- Docker.
- Docker Compose.

---

## Como rodar o projeto

### 1. Clone o repositório 
```bash
git clone https://github.com/MarceloPalmeira/cbo_airflow.git
cd cbo_airflow
```

### 2. Suba os serviços
```bash
docker compose up --build
```

Aguarde o PostgreSQL e o Airflow inicializarem (leva ~30 segundos). A interface web estará disponível em:

🔗 http://localhost:8081

---

### 3. Inicializar banco de dados do Airflow 

```bash
docker compose run airflow airflow db init
```

---

### 4. Criar usuário para login no Airflow

```bash
docker compose run airflow airflow users create \
  --username admin \
  --firstname Admin \
  --lastname Admin \
  --role Admin \
  --email admin@example.com \
  --password admin
```

---

### 5. Acessar o Airflow

Acesse: [http://localhost:8081](http://localhost:8081)  
Login: `admin`  
Senha: `admin`

---

## Como rodar as DAGs

Na interface web:

1. Ative as DAGs (`toggle` azul à esquerda do nome)
2. Clique no nome da DAG
3. Clique no botão **"Trigger DAG"** (▶️)
4. Acompanhe os logs se desejar

---

## Conexão com o Banco de Dados

Você pode acessar o banco PostgreSQL usando ferramentas como **DBeaver** ou **PgAdmin**.

- **Host**: `localhost`
- **Porta**: `5433`
- **Usuário**: `airflow`
- **Senha**: `airflow`
- **Banco de dados**: `airflow`

Se estiver usando Docker Desktop, você também pode usar o **container name** como host interno (`postgres`).

---

## Possíveis Problemas

- **Erro: password authentication failed for user 'airflow'**  
  Verifique se a conexão está usando exatamente: usuário `airflow`, senha `airflow` e banco `airflow`.

- **Interface do Airflow não carrega (aparece PostgreSQL EDB)**  
  Isso acontece quando o container do Airflow ainda não subiu. Espere um pouco e atualize.

- **Conflito de portas**  
  Verifique se já tem algum outro PostgreSQL rodando na porta `5432`. Se tiver, altere a porta no `docker-compose.yml`.

---
