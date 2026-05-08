# Documentação Técnica do Projeto ETL GitHub + StackOverflow

## Visão Geral

Este projeto implementa um pipeline ETL para extrair dados do GitHub e do StackOverflow, carregar dados brutos em um banco de dados PostgreSQL, transformar esses dados em tabelas relacionais e gerar indicadores analíticos de nível gold exibidos em um dashboard Streamlit.

O projeto está organizado em três camadas principais:

- `etl/`: código de extração, transformação e carregamento
- `dashboard/`: aplicação Streamlit para exploração e visualização dos dados
- `database/`: esquemas de banco de dados usados para as tabelas raw, silver e golden

## Arquitetura Geral

### 1. Extração (Extract)

Responsável por coletar dados das APIs externas.

Entrypoint:
- `etl/main_extract.py`

Principais módulos:
- `etl/extract/github_extractor.py`
- `etl/extract/stackoverflow_extractor.py`
- `etl/extract/rate_limit.py`

Fluxo:
- Busca repositórios no GitHub com mais de 50.000 estrelas
- Para os primeiros 10 repositórios, coleta commits, issues e pull requests
- Busca as perguntas e respostas mais votadas do StackOverflow
- Armazena os resultados JSON em tabelas brutas no PostgreSQL

### 2. Transformação (Transform)

Converte dados brutos em tabelas relacionais e normalizadas.

Entrypoint:
- `etl/main_transform.py`

Principais módulos:
- `etl/transform/github_transform.py`
- `etl/transform/stackoverflow_transform.py`
- `etl/transform/gold_transform.py` (funções utilitárias de transformação não utilizadas diretamente no pipeline)
- `etl/transform/integrated_transform.py` (placeholder vazio)
- `etl/transform/validators.py` (placeholder vazio)

Fluxo:
- Lê os payloads mais recentes das tabelas `github_raw` e `stackoverflow_raw`
- Converte JSON em `pandas.DataFrame`
- Popula as tabelas silver:
  - `github_repositories`
  - `github_commits`
  - `github_issues`
  - `github_pull_requests`
  - `stack_questions`
  - `stack_answers`

### 3. Carregamento e Gold Analytics

Gera tabelas de agregação de nível gold e persistência para consumo analítico.

Entrypoint:
- `etl/main_gold.py`

Módulo principal:
- `etl/gold/gold_builder.py`

Fluxo gold:
- `top_languages()`: extrai as 5 linguagens mais usadas em `github_repositories`
- `repository_activity()`: agrupa contagens de commits, issues e PRs por repositório
- `stackoverflow_topics()`: calcula temas de perguntas com maior volume no StackOverflow
- `github_stackoverflow_correlation()`: relaciona linguagens GitHub com tags de StackOverflow

### 4. Dashboard de Visualização

Apresenta os resultados gold de forma interativa usando Streamlit.

Arquivo principal:
- `dashboard/app.py`

Módulos de suporte:
- `dashboard/queries.py`
- `dashboard/charts.py`
- `dashboard/insights.py`
- `dashboard/database.py`

A aplicação consome as tabelas de visualização e cria:
- métricas em cards
- gráficos de barras
- gráfico de dispersão de correlação
- tabela de atividade de repositórios
- texto de insights gerados automaticamente

## Estrutura de Arquivos do Projeto

### `etl/`

- `main_extract.py`: executa a extração completa e grava em tabelas brutas
- `main_transform.py`: executa as transformações e grava em tabelas silver
- `main_load.py`: atualmente vazio, atuando como placeholder
- `main_gold.py`: executa os cálculos gold e grava em tabelas de análise
- `extract/`: coletoras de API
- `transform/`: classes de transformação de dados
- `load/`: classes de carregamento em banco de dados
- `gold/`: geração de dados gold
- `utils/`: configurações, engine SQL e logger

### `dashboard/`

- `app.py`: front-end Streamlit
- `queries.py`: consultas SQL para carregar tabelas gold
- `charts.py`: componentes Plotly
- `insights.py`: geração de observações de negócios
- `database.py`: engine SQL para o dashboard
- `pages/`: esqueleto de páginas adicionais (atualmente vazio)

### `database/`

- `raw_schema.sql`: define tabelas brutas `github_raw` e `stackoverflow_raw`
- `silver_schema.sql`: define tabelas transformadas GitHub/StackOverflow
- `golden_schema.sql`: define tabelas analíticas gold

## Detalhamento de Módulos e Funções

### `etl/extract/github_extractor.py`

Classe: `GitHubExtractor`

Funções:
- `search_repositories()`: consulta o endpoint `/search/repositories` do GitHub para encontrar repositórios populares
- `get_commits(owner, repo)`: obtém commits de um repositório específico
- `get_issues(owner, repo)`: obtém issues de um repositório específico
- `get_pull_requests(owner, repo)`: obtém PRs de um repositório específico

Observações:
- Usa o token GitHub de `etl.utils.config.GITHUB_TOKEN`
- Chama `handle_rate_limit()` para gerenciar `X-RateLimit-Remaining`
- Retorna JSON bruto
- Há funções duplicadas no final do arquivo que não são métodos da classe e provavelmente são resquícios de cópia/cola

### `etl/extract/stackoverflow_extractor.py`

Classe: `StackOverflowExtractor`

Funções:
- `get_questions()`: consulta `/questions` para perguntas mais votadas do StackOverflow
- `get_answers()`: consulta `/answers` para respostas mais votadas

Observações:
- Usa o endpoint da API `https://api.stackexchange.com/2.3`
- Retorna JSON bruto
- Também contém uma função solta `get_answers(self)` duplicada fora da classe

### `etl/extract/rate_limit.py`

Função:
- `handle_rate_limit(response)`: lê os headers `X-RateLimit-Remaining` e `X-RateLimit-Reset`
- Se o limite estiver zerado, dorme até o reset ser atingido

### `etl/load/raw_loader.py`

Classe: `RawLoader`

Função:
- `save_raw_data(table_name, endpoint, payload)`: grava payload JSON como texto em tabela SQL bruta
- Usa `pandas.DataFrame.to_sql()` com `if_exists='append'`
- Tabela de destino pode ser `github_raw` ou `stackoverflow_raw`

### `etl/load/silver_loader.py`

Classe: `SilverLoader`

Função:
- `load(dataframe, table_name)`: grava um `DataFrame` transformado em uma tabela silver
- Usa `if_exists='append'`

### `etl/transform/github_transform.py`

Classe: `GitHubTransform`

Funções:
- `repositories(raw_data)`: mapeia repositórios GitHub para colunas relacionais
  - Campos: `repo_id`, `name`, `owner`, `language`, `stars`, `forks`, `open_issues`, `created_at`
  - Normaliza `language` para "Unknown" quando ausente
- `commits(commits_raw, repo_name)`: transforma commits para colunas de registro
  - Campos: `sha`, `repo_name`, `author_name`, `commit_message`, `commit_date`
- `issues(issues_raw, repo_name)`: filtra issues removendo PRs e extrai metadata
  - Campos: `issue_id`, `repo_name`, `title`, `state`, `created_at`
- `pull_requests(prs_raw, repo_name)`: transforma PRs em registros de pull request
  - Campos: `pr_id`, `repo_name`, `title`, `state`, `created_at`

### `etl/transform/stackoverflow_transform.py`

Classe: `StackOverflowTransform`

Funções:
- `questions(raw_data)`: transforma perguntas em registros
  - Campos: `question_id`, `title`, `tags`, `answer_count`, `score`, `creation_date`
  - Concatena `tags` em string separada por vírgulas
- `answers(raw_data)`: transforma respostas em registros
  - Campos: `answer_id`, `question_id`, `score`, `creation_date`

### `etl/transform/gold_transform.py`

Classe: `GoldTransform`

Funções auxiliares para cálculos analíticos em pandas:
- `top_languages(repositories_df)`
- `repo_activity(commits_df, issues_df, prs_df)`
- `stackoverflow_topics(questions_df)`
- `github_stackoverflow_correlation(repositories_df, questions_df)`

Este módulo não é usado diretamente pelo pipeline principal atual, mas oferece transformações de agregação em memória.

### `etl/gold/gold_builder.py`

Classe: `GoldBuilder`

Funções:
- `top_languages()`: cria `gold_top_languages` a partir de `github_repositories`
- `repository_activity()`: cria `gold_repository_activity` associando commits, issues e PRs
- `stackoverflow_topics()`: cria `gold_stackoverflow_topics` a partir de `stack_questions`
- `github_stackoverflow_correlation()`: cria `github_stackoverflow_correlation`

Detalhes:
- `github_stackoverflow_correlation()` usa `sqlalchemy.text()` com conexão explícita
- As tabelas gold são gravadas com `if_exists='replace'`

### `etl/utils/config.py`

Variáveis de ambiente carregadas com `python-dotenv`:
- `GITHUB_TOKEN`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

### `etl/utils/database.py`

Cria `SQLAlchemy` engine para PostgreSQL usando parâmetros separados do `.env`.

### `etl/utils/logger.py`

Configura logging básico para arquivo `logs/pipeline.log`.

### `dashboard/database.py`

Cria `SQLAlchemy` engine a partir de `DATABASE_URL` carregado de `.env` na raiz.

### `dashboard/queries.py`

Funções de consulta:
- `get_top_languages()` lê tabela `top_languages`
- `get_repo_activity()` lê tabela `repo_activity`
- `get_stackoverflow_topics()` lê tabela `stackoverflow_topics`
- `get_correlation()` lê tabela `github_stackoverflow_correlation`

### `dashboard/charts.py`

Funções que retornam objetos Plotly:
- `languages_chart(df)`: gráfico de barras com as top linguagens e quantidade de repositórios
- `topics_chart(df)`: gráfico de barras com os top 10 tópicos do StackOverflow e menções
- `correlation_chart(df)`: gráfico de linha mostrando a correlação entre linguagens (eixo X em ordem alfabética) e quantidade de repositórios no GitHub (eixo Y)
  - Cada ponto da linha exibe o valor exato de repositórios
  - Facilita a visualização de tendências entre as linguagens

### `dashboard/insights.py`

Função:
- `generate_insights(top_languages_df, topics_df)`: cria markdown com:
  - linguagem mais popular
  - tópico mais discutido
  - relação entre GitHub e StackOverflow
  - tendência de engajamento técnico

### `dashboard/app.py`

Ponto de entrada do dashboard Streamlit.
- configura `st.set_page_config`
- carrega dados com consultas
- exibe métricas, gráficos e tabela de atividade
- renderiza insights em markdown

## Esquema de Banco de Dados

### Raw (`database/raw_schema.sql`)

- `github_raw`
  - `id`, `endpoint`, `extracted_at`, `payload`
- `stackoverflow_raw`
  - `id`, `endpoint`, `extracted_at`, `payload`

### Silver (`database/silver_schema.sql`)

GitHub:
- `github_repositories`
- `github_commits`
- `github_issues`
- `github_pull_requests`

StackOverflow:
- `stack_questions`
- `stack_answers`

### Golden (`database/golden_schema.sql`)

- `top_languages`
- `repo_activity`
- `stackoverflow_topics`
- `github_stackoverflow_correlation`

## Funcionalidades Implementadas

- Extração de dados do GitHub (repositórios, commits, issues, pull requests)
- Extração de dados do StackOverflow (perguntas e respostas)
- Persistência de payloads brutos em tabelas raw
- Transformação de JSON em tabelas relacionais silver
- Geração de indicadores gold e correlações entre GitHub e StackOverflow
- Dashboard de visualização com Streamlit e Plotly
  - Gráfico de barras para top linguagens no GitHub
  - Gráfico de barras para top tópicos no StackOverflow
  - Gráfico de linha para correlação entre linguagens e repositórios (alfabético no eixo X)
  - Tabela de atividade de repositórios
  - Cards de métricas principais
  - Geração automática de insights
- Tratamento de rate limit da API do GitHub
- Log de execução em `logs/pipeline.log`

## Observações Técnicas

- O módulo `etl/main_load.py` está presente, mas atualmente vazio.
- O dashboard depende de `DATABASE_URL` no `.env`, enquanto o ETL usa `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` e `DB_NAME`.
- Há módulos de página em `dashboard/pages/` vazios, sugerindo expansão futura para navegação multi-page.
- O pipeline atual grava em tabelas já existentes no banco. A criação das tabelas pode ser feita a partir dos scripts SQL em `database/`.

## Pontos de Melhoria

- Unificar a configuração de banco de dados entre `etl/utils/database.py` e `dashboard/database.py`
- Implementar `etl/main_load.py` ou renomear/remover se não for necessário
- Remover funções duplicadas e não utilizadas em `github_extractor.py` e `stackoverflow_extractor.py`
- Preencher `etl/transform/integrated_transform.py` e `etl/transform/validators.py` com lógica de validação e integração
- Adicionar tratamento de exceções mais robusto nas requisições HTTP
- Normalizar storage de data/hora para UTC e validar payloads JSON antes de salvar

## Como Rodar

1. Criar o arquivo `.env` com as variáveis esperadas
2. Executar `etl/main_extract.py` para extrair e salvar dados brutos
3. Executar `etl/main_transform.py` para transformar e carregar tabelas silver
4. Executar `etl/main_gold.py` para gerar as tabelas gold
5. Executar o dashboard Streamlit com `streamlit run dashboard/app.py`
