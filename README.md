# ETL GitHub + StackOverflow Analytics

Dashboard analítico integrado que coleta, processa e visualiza dados do GitHub e do StackOverflow em uma aplicação web interativa.

## 🎯 Objetivo

Analisar a correlação entre linguagens de programação populares no GitHub e tópicos mais discutidos no StackOverflow, fornecendo insights sobre tendências tecnológicas e engajamento da comunidade.

## ✨ Funcionalidades

- **Extração de Dados**: Coleta automática de repositórios, commits, issues e pull requests do GitHub
- **API StackOverflow**: Importação de perguntas e respostas mais votadas
- **Pipeline ETL Robusto**: Tratamento de rate limit, transformação e normalização de dados
- **Dashboard Interativo**: Visualização em tempo real com gráficos e métricas
- **Análise Correlacional**: Relaciona linguagens GitHub com tópicos StackOverflow
- **Insights Automatizados**: Geração de observações de negócio baseadas nos dados

## 🛠️ Stack Tecnológico

### Backend ETL
- **Python 3.x** - Linguagem principal
- **Pandas** - Manipulação e transformação de dados
- **SQLAlchemy** - ORM para acesso a banco de dados
- **Requests** - Cliente HTTP para APIs

### Banco de Dados
- **PostgreSQL** - Persistência de dados raw, silver e golden

### Frontend
- **Streamlit** - Framework web para visualização de dados
- **Plotly** - Gráficos interativos

### APIs Externas
- **GitHub API** - Dados de repositórios, commits, issues, PRs
- **StackExchange API** - Dados de perguntas e respostas

## 📁 Estrutura do Projeto

```
etl-github-e-stackoverflow/
├── etl/                          # Pipeline de ETL
│   ├── extract/                  # Extração de dados
│   │   ├── github_extractor.py   # Coleta GitHub
│   │   ├── stackoverflow_extractor.py
│   │   └── rate_limit.py         # Gerenciamento de rate limit
│   ├── transform/                # Transformação de dados
│   │   ├── github_transform.py
│   │   ├── stackoverflow_transform.py
│   │   └── gold_transform.py
│   ├── load/                     # Carregamento em banco
│   │   ├── raw_loader.py
│   │   ├── silver_loader.py
│   │   └── gold_loader.py
│   ├── gold/                     # Geração de dados analíticos
│   │   └── gold_builder.py
│   ├── utils/                    # Utilitários
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logger.py
│   ├── main_extract.py           # Entrypoint de extração
│   ├── main_transform.py         # Entrypoint de transformação
│   └── main_gold.py              # Entrypoint de gold analytics
│
├── dashboard/                    # Aplicação Streamlit
│   ├── app.py                    # Dashboard principal
│   ├── queries.py                # Consultas ao banco
│   ├── charts.py                 # Componentes de gráficos
│   ├── insights.py               # Geração de insights
│   ├── database.py               # Conexão com BD
│   └── pages/                    # Páginas adicionais (multi-page)
│
├── database/                     # Esquemas SQL
│   ├── raw_schema.sql            # Tabelas brutas (github_raw, stackoverflow_raw)
│   ├── silver_schema.sql         # Tabelas relacionais (github_*, stack_*)
│   └── golden_schema.sql         # Tabelas analíticas (gold_*, correlation)
│
├── logs/                         # Logs da execução
├── .env                          # Variáveis de ambiente
└── DOCUMENTATION.md              # Documentação técnica detalhada
```

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8+
- PostgreSQL instalado e rodando
- Conta GitHub (token de acesso)
- Conexão com internet

### 1. Configuração do Ambiente

Clone o repositório:
```bash
git clone https://github.com/seu-usuario/etl-github-e-stackoverflow.git
cd etl-github-e-stackoverflow
```

Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados

Crie um banco PostgreSQL:
```sql
CREATE DATABASE github_stackoverflow;
```

Crie as tabelas executando os scripts SQL em ordem:
```bash
psql -U seu_usuario -d github_stackoverflow -f database/raw_schema.sql
psql -U seu_usuario -d github_stackoverflow -f database/silver_schema.sql
psql -U seu_usuario -d github_stackoverflow -f database/golden_schema.sql
```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:
```env
GITHUB_TOKEN=seu_token_github
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=github_stackoverflow
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/github_stackoverflow
```

**Como gerar um GitHub Token:**
1. Acesse https://github.com/settings/tokens
2. Clique em "Generate new token"
3. Selecione permissões: `public_repo`, `read:user`
4. Copie o token e adicione ao `.env`

### 4. Executar o Pipeline ETL

Execute os três estágios em ordem:

**Estágio 1: Extração**
```bash
python -m etl.main_extract
```
Coleta dados brutos do GitHub e StackOverflow.

**Estágio 2: Transformação**
```bash
python -m etl.main_transform
```
Transforma dados brutos em tabelas relacionais.

**Estágio 3: Gold Analytics**
```bash
python -m etl.main_gold
```
Gera tabelas de análise e correlações.

### 5. Iniciar o Dashboard

```bash
streamlit run dashboard/app.py
```

A aplicação será aberta em `http://localhost:8501`

## 📊 Dashboard

O dashboard exibe:

- **Métricas Principais**
  - Linguagem mais popular no GitHub
  - Tópico mais discutido no StackOverflow
  - Quantidade de tecnologias correlacionadas

- **Gráficos**
  - Barras: Top linguagens por número de repositórios
  - Barras: Top tópicos StackOverflow por menções
  - Scatter: Correlação GitHub vs StackOverflow

- **Tabelas**
  - Atividade de repositórios (commits, issues, PRs)

- **Insights**
  - Observações automáticas sobre tendências tecnológicas
  - Relação entre popularidade e engajamento

## 🔄 Fluxo de Dados

```
GitHub API / StackExchange API
    ↓
[Extração] → Raw Tables (github_raw, stackoverflow_raw)
    ↓
[Transformação] → Silver Tables (github_*, stack_*)
    ↓
[Gold Analytics] → Gold Tables (top_*, correlation, topics)
    ↓
[Dashboard Streamlit] → Visualização
```

## 📈 Fluxo do Pipeline ETL

1. **Extract**: Requisita dados das APIs e armazena JSON bruto
2. **Raw**: Persiste payloads em tabelas de auditoria
3. **Transform**: Normaliza JSON em tabelas relacionais
4. **Silver**: Armazena dados transformados
5. **Gold**: Agrega dados para análise
6. **Visualization**: Renderiza gráficos e insights

## ⚙️ Componentes Principais

### `GitHubExtractor`
Coleta repositórios populares e seus metadados:
- Busca por repositórios com mais de 50.000 stars
- Extrai commits, issues e pull requests

### `StackOverflowExtractor`
Coleta dados do StackOverflow:
- Perguntas mais votadas
- Respostas mais votadas

### `GitHubTransform` e `StackOverflowTransform`
Normalizam dados JSON em tabelas relacionais com tipos de dados apropriados.

### `GoldBuilder`
Gera tabelas analíticas:
- Top 5 linguagens mais usadas
- Atividade de repositórios
- Tópicos do StackOverflow
- Correlação entre tecnologias

### Dashboard Streamlit
Interface web com:
- Métricas em cards
- Gráficos interativos Plotly
- Tabelas dinâmicas
- Insights em markdown

## 🔒 Tratamento de Rate Limit

O sistema monitora o header `X-RateLimit-Remaining` da GitHub API e aguarda automaticamente quando o limite é atingido, respeitando o tempo de reset.

## 📝 Logging

Todos os eventos são registrados em `logs/pipeline.log` com:
- Timestamp
- Nível (INFO, WARNING, ERROR)
- Mensagem descritiva

## 🐛 Troubleshooting

### "GITHUB_TOKEN not found"
Verificar se o token está definido no `.env` e se o arquivo está na raiz do projeto.

### "Cannot connect to PostgreSQL"
Verificar se PostgreSQL está rodando e se as credenciais estão corretas.

### "Rate limit exceeded"
Aguardar o tempo de reset exibido no log ou usar um token com permissões maiores.

### "Table not found"
Executar os scripts SQL em `database/` para criar as tabelas.

## 📚 Documentação Técnica

Para documentação detalhada sobre arquitetura, módulos e funções, consulte [DOCUMENTATION.md](./DOCUMENTATION.md).

## 🤝 Contribuindo

Para contribuir com melhorias:
1. Crie uma branch para sua feature
2. Commit com mensagens descritivas
3. Push para a branch
4. Abra um Pull Request

## 📋 Roadmap

- [ ] Preencher páginas multi-page do dashboard
- [ ] Implementar validação de dados com `validators.py`
- [ ] Adicionar testes unitários
- [ ] Suporte a cache para melhor performance
- [ ] Alertas baseados em anomalias
- [ ] Export de relatórios em PDF

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como projeto de análise de dados e ETL.

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Última atualização**: Maio 2026