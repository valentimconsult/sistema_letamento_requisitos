# Documentacao Tecnica - Sistema BI de Levantamento de Requisitos

## Visao Geral

Este sistema foi desenvolvido para gerenciar requisitos em projetos de Business Intelligence, oferecendo uma solucao completa com front-end e back-end separados, utilizando tecnologias modernas e boas praticas de desenvolvimento.

## Arquitetura

### Stack Tecnologico

#### Backend
- **FastAPI**: Framework web moderno para Python
- **PostgreSQL**: Banco de dados relacional robusto
- **SQLAlchemy**: ORM para Python
- **JWT**: Autenticacao baseada em tokens
- **Pydantic**: Validacao de dados
- **Alembic**: Migracoes de banco de dados

#### Frontend
- **React 18**: Biblioteca JavaScript para interfaces
- **TypeScript**: Tipagem estatica
- **Vite**: Build tool e dev server
- **Tailwind CSS**: Framework CSS utilitario
- **React Router**: Roteamento
- **React Query**: Gerenciamento de estado do servidor
- **React Hook Form**: Formularios

#### Infraestrutura
- **Docker**: Containerizacao
- **Docker Compose**: Orquestracao de containers
- **Nginx**: Proxy reverso
- **PostgreSQL**: Banco de dados

### Estrutura do Projeto

```
sistema-bi-requisitos/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/v1/            # Endpoints da API
│   │   ├── core/              # Configuracoes centrais
│   │   ├── models/            # Modelos do banco
│   │   └── schemas/           # Schemas Pydantic
│   ├── requirements.txt       # Dependencias Python
│   ├── Dockerfile            # Container do backend
│   └── init.sql              # Script de inicializacao
├── frontend/                  # Aplicacao React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── hooks/            # Custom hooks
│   │   ├── pages/            # Paginas da aplicacao
│   │   ├── services/         # Servicos da API
│   │   └── types/            # Tipos TypeScript
│   ├── package.json          # Dependencias Node.js
│   └── Dockerfile            # Container do frontend
├── nginx/                    # Configuracao do proxy
│   └── nginx.conf
├── docker-compose.yml        # Orquestracao
├── env.example              # Variaveis de ambiente
└── README.md                # Documentacao principal
```

## Funcionalidades Principais

### 1. Autenticacao e Autorizacao
- Login/logout com JWT
- Controle de permissoes por roles
- Gerenciamento de usuarios
- Recuperacao de senha (preparado)

### 2. Gestao de Projetos
- CRUD completo de projetos
- Status de projetos (Em andamento, Concluido, Cancelado, Pausado)
- Prioridades (Baixa, Media, Alta, Critica)
- Associacao de requisitos
- Progresso automatico baseado em requisitos

### 3. Gestao de Requisitos
- CRUD completo de requisitos
- Tipos de requisitos (Funcional, Nao Funcional, Regra de Negocio)
- Prioridades (Baixa, Media, Alta, Critica)
- Status (Pendente, Em Analise, Aprovado, Em Desenvolvimento, Concluido, Cancelado)
- Campos dinamicos personalizaveis
- Atribuicao a usuarios
- Controle de vencimento

### 4. Campos Dinamicos
- Configuracao flexivel de campos
- Tipos: texto, numero, data, selecao, textarea, booleano
- Aplicacao a projetos ou requisitos
- Validacao configuravel

### 5. Relatorios
- Dashboard com metricas
- Exportacao em CSV, Excel, PDF
- Relatorios por projeto
- Graficos e visualizacoes

### 6. Seguranca
- Autenticacao JWT
- Criptografia de senhas (bcrypt)
- CORS configurado
- Rate limiting
- Headers de seguranca
- Validacao de entrada

## Modelos de Dados

### Usuario (User)
```sql
- id: UUID (PK)
- username: String (unique)
- email: String (unique)
- password_hash: String
- first_name: String
- last_name: String
- role: String
- permissions: JSON
- is_active: Boolean
- is_superuser: Boolean
- last_login: DateTime
- created_at: DateTime
- updated_at: DateTime
```

### Projeto (Project)
```sql
- id: UUID (PK)
- name: String
- description: Text
- status: String
- priority: String
- start_date: DateTime
- end_date: DateTime
- budget: String
- client_name: String
- is_active: Boolean
- created_by: UUID (FK -> User)
- created_at: DateTime
- updated_at: DateTime
```

### Requisito (Requirement)
```sql
- id: UUID (PK)
- title: String
- description: Text
- type: String
- priority: String
- status: String
- complexity: String
- estimated_hours: String
- actual_hours: String
- due_date: DateTime
- completion_date: DateTime
- dynamic_fields: JSON
- project_id: UUID (FK -> Project)
- assigned_to: UUID (FK -> User)
- created_by: UUID (FK -> User)
- created_at: DateTime
- updated_at: DateTime
```

### Campo Dinamico (DynamicFieldDefinition)
```sql
- id: UUID (PK)
- field_name: String
- field_type: String
- field_label: String
- field_description: Text
- options: JSON
- is_required: Boolean
- is_active: Boolean
- applies_to: String
- order_index: String
- validation_rules: JSON
- created_at: DateTime
- updated_at: DateTime
```

## API Endpoints

### Autenticacao
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/register` - Registro
- `GET /api/v1/auth/me` - Usuario atual
- `POST /api/v1/auth/refresh-token` - Renovar token

### Usuarios
- `GET /api/v1/users/` - Listar usuarios
- `GET /api/v1/users/{id}` - Obter usuario
- `POST /api/v1/users/` - Criar usuario
- `PUT /api/v1/users/{id}` - Atualizar usuario
- `DELETE /api/v1/users/{id}` - Deletar usuario

### Projetos
- `GET /api/v1/projects/` - Listar projetos
- `GET /api/v1/projects/{id}` - Obter projeto
- `POST /api/v1/projects/` - Criar projeto
- `PUT /api/v1/projects/{id}` - Atualizar projeto
- `DELETE /api/v1/projects/{id}` - Deletar projeto

### Requisitos
- `GET /api/v1/requirements/` - Listar requisitos
- `GET /api/v1/requirements/{id}` - Obter requisito
- `POST /api/v1/requirements/` - Criar requisito
- `PUT /api/v1/requirements/{id}` - Atualizar requisito
- `DELETE /api/v1/requirements/{id}` - Deletar requisito

### Campos Dinamicos
- `GET /api/v1/dynamic-fields/` - Listar campos
- `GET /api/v1/dynamic-fields/{id}` - Obter campo
- `POST /api/v1/dynamic-fields/` - Criar campo
- `PUT /api/v1/dynamic-fields/{id}` - Atualizar campo
- `DELETE /api/v1/dynamic-fields/{id}` - Deletar campo

### Relatorios
- `GET /api/v1/reports/dashboard` - Dados do dashboard
- `GET /api/v1/reports/projects/export` - Exportar projetos
- `GET /api/v1/reports/requirements/export` - Exportar requisitos

## Configuracao de Desenvolvimento

### Pre-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

### Instalacao

1. **Clone o repositorio**
```bash
git clone <url-do-repositorio>
cd sistema-bi-requisitos
```

2. **Configure as variaveis de ambiente**
```bash
cp env.example .env
# Edite o arquivo .env com suas configuracoes
```

3. **Execute com Docker**
```bash
docker-compose up -d
```

4. **Acesse a aplicacao**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentacao API: http://localhost:8000/docs

### Desenvolvimento Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Seguranca

### Implementacoes de Seguranca
- **Autenticacao JWT**: Tokens com expiracao
- **Criptografia**: Senhas hash com bcrypt
- **CORS**: Configurado para origens permitidas
- **Rate Limiting**: Protecao contra ataques
- **Validacao**: Entrada de dados validada
- **Headers de Seguranca**: XSS, CSRF, etc.
- **Logs de Auditoria**: Todas as acoes logadas

### Boas Praticas
- Senhas fortes obrigatorias
- Sessoes com expiracao
- Logs de acesso
- Backup automatico
- Monitoramento de performance

## Deploy em Producao

### Configuracao de Producao

1. **Configure o servidor**
```bash
# Instale Docker e Docker Compose
sudo apt update
sudo apt install docker.io docker-compose
```

2. **Clone e configure**
```bash
git clone <repositorio>
cd sistema-bi-requisitos
cp env.example .env
# Edite .env com configuracoes de producao
```

3. **Execute**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Configuracoes de Producao
- Use HTTPS com certificados SSL
- Configure backup automatico do banco
- Monitore logs e performance
- Configure firewall adequadamente
- Use variaveis de ambiente seguras

## Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## Monitoramento

### Logs
- Logs estruturados com structlog
- Rotacao automatica de logs
- Niveis de log configuraveis

### Metricas
- Health checks
- Performance monitoring
- Error tracking

## Manutencao

### Backup
- Backup automatico do PostgreSQL
- Backup de arquivos de upload
- Retencao configuravel

### Atualizacoes
- Migracoes de banco com Alembic
- Versionamento semantico
- Rollback procedures

## Contribuicao

### Padroes de Codigo
- PEP 8 para Python
- ESLint para JavaScript/TypeScript
- Prettier para formatacao
- TypeScript strict mode

### Git Workflow
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudancas
4. Push para a branch
5. Abra um Pull Request

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Para suporte tecnico:
- Email: suporte@sistema-bi.com
- Documentacao: https://docs.sistema-bi.com
- Issues: GitHub Issues
