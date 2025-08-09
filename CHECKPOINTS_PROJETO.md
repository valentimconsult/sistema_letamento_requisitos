# Sistema de Checkpoints - Navegacao Rapida do Projeto

## 🎯 Objetivo
Este arquivo serve como "mapa de navegação" para identificar rapidamente areas problematicas e funcionalidades especificas sem necessidade de escaneamento completo do projeto.

## 🚨 CHECKPOINTS CRITICOS (Areas que podem dar problemas)

### 1. AUTENTICACAO E LOGIN
**Palavras-chave**: `auth`, `login`, `jwt`, `security`, `password`
**Arquivos relacionados**:
- `backend/app/core/security.py` - Logica de JWT e criptografia
- `backend/app/api/v1/endpoints/auth.py` - Endpoints de autenticacao
- `frontend/src/hooks/useAuth.tsx` - Hook de autenticacao
- `frontend/src/pages/LoginPage.tsx` - Pagina de login

**Problemas comuns**:
- Token JWT expirado
- Criptografia de senha
- Validacao de credenciais
- Persistencia de sessao

### 2. CARGA E UPLOAD DE ARQUIVOS
**Palavras-chave**: `upload`, `file`, `multipart`, `form-data`
**Arquivos relacionados**:
- `backend/app/api/v1/endpoints/requirements.py` - Upload de documentos
- `backend/uploads/` - Diretorio de arquivos
- `frontend/src/components/` - Componentes de upload

**Problemas comuns**:
- Tamanho maximo de arquivo
- Tipos de arquivo permitidos
- Armazenamento de arquivos
- Permissoes de acesso

### 3. GERACAO DE RELATORIOS
**Palavras-chave**: `report`, `pdf`, `excel`, `export`, `generate`
**Arquivos relacionados**:
- `backend/app/api/v1/endpoints/reports.py` - Geracao de relatorios
- `backend/app/core/` - Configuracoes de relatorios
- `frontend/src/pages/ReportsPage.tsx` - Interface de relatorios

**Problemas comuns**:
- Formato de saida (PDF/Excel)
- Dados para relatorio
- Performance de geracao
- Download de arquivos

### 4. BANCO DE DADOS E MODELOS
**Palavras-chave**: `database`, `model`, `sqlalchemy`, `postgresql`
**Arquivos relacionados**:
- `backend/app/core/database.py` - Conexao com banco
- `backend/app/models/` - Modelos de dados
- `backend/init.sql` - Scripts de inicializacao
- `docker-compose.yml` - Configuracao do PostgreSQL

**Problemas comuns**:
- Conexao com banco
- Migracoes de schema
- Performance de queries
- Backup e restauracao

### 5. FRONTEND E INTERFACE
**Palavras-chave**: `react`, `typescript`, `component`, `state`, `api`
**Arquivos relacionados**:
- `frontend/src/App.tsx` - Aplicacao principal
- `frontend/src/components/` - Componentes reutilizaveis
- `frontend/src/pages/` - Paginas da aplicacao
- `frontend/src/services/api.ts` - Servicos de API

**Problemas comuns**:
- Renderizacao de componentes
- Gerenciamento de estado
- Chamadas de API
- Responsividade

## 🔍 SISTEMA DE BUSCA RAPIDA

### Para problemas de AUTENTICACAO:
```bash
grep -r "auth\|login\|jwt\|security" backend/app/ frontend/src/
```

### Para problemas de UPLOAD:
```bash
grep -r "upload\|file\|multipart" backend/app/ frontend/src/
```

### Para problemas de RELATORIOS:
```bash
grep -r "report\|pdf\|excel\|export" backend/app/ frontend/src/
```

### Para problemas de BANCO:
```bash
grep -r "database\|model\|sqlalchemy" backend/app/
```

## 📋 CHECKLIST DE VERIFICACAO RAPIDA

### ✅ Sistema Funcionando
- [ ] Backend rodando na porta 8000
- [ ] Frontend rodando na porta 4000
- [ ] Banco PostgreSQL rodando na porta 5432
- [ ] Nginx funcionando como proxy

### ❌ Problemas Comuns
- [ ] Erro de conexao com banco
- [ ] Token JWT invalido
- [ ] Upload de arquivo falhando
- [ ] Relatorio nao gerando
- [ ] Frontend nao carregando

## 🚀 COMANDOS DE DIAGNOSTICO RAPIDO

### Verificar Status dos Containers:
```bash
docker-compose ps
```

### Ver Logs de Erro:
```bash
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep ERROR
docker-compose logs postgres | grep ERROR
```

### Verificar Conectividade:
```bash
curl http://localhost:8000/health
curl http://localhost:4000
```

### Verificar Banco de Dados:
```bash
docker-compose exec postgres psql -U admin -d sistema_bi -c "SELECT version();"
```

## 🎯 AREAS DE FOCO POR TIPO DE PROBLEMA

### Problema de Performance:
1. Verificar logs do backend
2. Analisar queries do banco
3. Verificar uso de memoria/CPU

### Problema de Interface:
1. Verificar console do navegador
2. Analisar logs do frontend
3. Verificar chamadas de API

### Problema de Dados:
1. Verificar conexao com banco
2. Analisar modelos de dados
3. Verificar schemas Pydantic

### Problema de Seguranca:
1. Verificar tokens JWT
2. Analisar permissoes
3. Verificar validacoes

## 📝 NOTAS IMPORTANTES

- **NUNCA** fazer full scan do projeto para problemas simples
- **SEMPRE** usar palavras-chave para localizar areas especificas
- **VERIFICAR** checkpoints antes de analisar codigo
- **USAR** comandos de diagnostico para problemas comuns
- **FOCO** em uma area por vez para evitar confusao

## 🔗 LINKS UTEIS

- **API Docs**: http://localhost:8000/docs
- **Adminer (Banco)**: http://localhost:8080
- **Frontend**: http://localhost:4000
- **Backend**: http://localhost:8000
