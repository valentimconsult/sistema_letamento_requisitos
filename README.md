# Sistema Web para Levantamento de Requisitos em Projetos de BI

Sistema completo para gerenciamento de requisitos em projetos de Business Intelligence, desenvolvido com FastAPI (backend) e React + TypeScript (frontend).

## 🚀 Funcionalidades

### Backend (FastAPI)
- **Autenticação e Autorização**: Sistema JWT completo
- **Gerenciamento de Usuários**: CRUD completo com roles e permissões
- **Gerenciamento de Projetos**: Criação, edição e visualização de projetos
- **Gerenciamento de Requisitos**: CRUD com campos dinâmicos
- **Campos Dinâmicos**: Sistema flexível para requisitos customizados
- **Relatórios**: Geração de relatórios em PDF e Excel
- **API RESTful**: Documentação automática com Swagger

### Frontend (React + TypeScript)
- **Interface Moderna**: Design responsivo com Tailwind CSS
- **Autenticação**: Login/logout com persistência de sessão
- **Dashboard**: Visão geral dos projetos e requisitos
- **Gerenciamento de Projetos**: Interface intuitiva para CRUD
- **Gerenciamento de Requisitos**: Formulários dinâmicos
- **Campos Dinâmicos**: Interface para configuração de campos customizados
- **Relatórios**: Visualização e download de relatórios

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **PostgreSQL**: Banco de dados relacional
- **Pydantic**: Validação de dados
- **JWT**: Autenticação segura
- **Uvicorn**: Servidor ASGI

### Frontend
- **React 18**: Biblioteca para interfaces
- **TypeScript**: Tipagem estática
- **Vite**: Build tool moderna
- **Tailwind CSS**: Framework CSS utilitário
- **React Router**: Roteamento
- **Axios**: Cliente HTTP
- **React Hook Form**: Gerenciamento de formulários
- **React Hot Toast**: Notificações

### Infraestrutura
- **Docker**: Containerização
- **Docker Compose**: Orquestração de containers
- **Nginx**: Proxy reverso
- **PostgreSQL**: Banco de dados

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Git para clonar o repositório

## 🚀 Instalação e Execução

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd sistema-bi-requisitos
```

### 2. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
# (opcional - as configurações padrão funcionam para desenvolvimento)
```

### 3. Execute o sistema
```bash
# Construa e inicie todos os serviços
docker-compose up --build -d

# Verifique se todos os containers estão rodando
docker-compose ps
```

### 4. Acesse o sistema
- **Frontend**: http://localhost:4000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Adminer (Banco de dados)**: http://localhost:8080

## 👤 Usuário Padrão

O sistema é inicializado com um usuário administrador:

- **Usuário**: admin
- **Senha**: admin123

## 📁 Estrutura do Projeto

```
sistema-bi-requisitos/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/v1/         # Endpoints da API
│   │   ├── core/           # Configurações centrais
│   │   ├── models/         # Modelos do banco de dados
│   │   └── schemas/        # Schemas Pydantic
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile         # Container do backend
├── frontend/              # Aplicação React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas da aplicação
│   │   ├── services/      # Serviços de API
│   │   └── types/         # Tipos TypeScript
│   ├── package.json       # Dependências Node.js
│   └── Dockerfile         # Container do frontend
├── nginx/                 # Configuração do proxy
├── docker-compose.yml     # Orquestração dos containers
└── README.md             # Este arquivo
```

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar todos os serviços
docker-compose down

# Reconstruir containers
docker-compose up --build

# Acessar container do backend
docker-compose exec backend bash

# Acessar container do frontend
docker-compose exec frontend sh
```

### Banco de Dados
```bash
# Fazer backup do banco
docker-compose exec postgres pg_dump -U admin sistema_bi > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U admin sistema_bi < backup.sql
```

## 📊 Funcionalidades Principais

### 1. Gerenciamento de Projetos
- Criar, editar e visualizar projetos
- Definir escopo e objetivos
- Acompanhar status e progresso

### 2. Gerenciamento de Requisitos
- Cadastrar requisitos funcionais e não funcionais
- Campos dinâmicos customizáveis
- Categorização e priorização

### 3. Campos Dinâmicos
- Criar campos customizados por projeto
- Suporte a diferentes tipos de dados
- Validação automática

### 4. Relatórios
- Geração de relatórios em PDF
- Exportação para Excel
- Gráficos e estatísticas

### 5. Sistema de Usuários
- Controle de acesso baseado em roles
- Permissões granulares
- Auditoria de ações

## 🔒 Segurança

- Autenticação JWT
- Criptografia de senhas
- Validação de entrada
- Proteção contra ataques comuns
- Logs de auditoria

## 📈 Monitoramento

- Logs estruturados
- Métricas de performance
- Health checks
- Tratamento de erros

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação da API em `/docs`
- Verifique os logs dos containers

---

**Desenvolvido com ❤️ para projetos de Business Intelligence**
