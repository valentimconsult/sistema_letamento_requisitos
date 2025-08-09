# Sistema de Busca Rapida - Localizacao de Problemas

## 🎯 COMO USAR ESTE SISTEMA

**NUNCA faça full scan do projeto!** Use estas buscas direcionadas para localizar problemas específicos.

## 🚨 PROBLEMAS DE AUTENTICACAO

### Buscar por problemas de JWT:
```bash
grep -r "jwt\|token\|expired" backend/app/core/ frontend/src/hooks/
```

### Buscar por problemas de login:
```bash
grep -r "login\|password\|credential" backend/app/api/v1/endpoints/ frontend/src/pages/
```

### Verificar arquivos de seguranca:
```bash
ls -la backend/app/core/security.py
ls -la backend/app/api/v1/endpoints/auth.py
```

## 📁 PROBLEMAS DE UPLOAD DE ARQUIVOS

### Buscar por problemas de upload:
```bash
grep -r "upload\|file\|multipart" backend/app/api/v1/endpoints/requirements.py
```

### Verificar configuracoes de arquivo:
```bash
grep -r "max_file_size\|allowed_types" backend/app/core/
```

### Verificar diretorio de uploads:
```bash
ls -la backend/uploads/
```

## 📊 PROBLEMAS DE RELATORIOS

### Buscar por problemas de geracao:
```bash
grep -r "report\|pdf\|excel" backend/app/api/v1/endpoints/reports.py
```

### Verificar dependencias de relatorio:
```bash
grep -r "reportlab\|openpyxl\|xlsxwriter" backend/requirements.txt
```

### Verificar logs de relatorio:
```bash
docker-compose logs backend | grep -i "report\|pdf\|excel"
```

## 🗄️ PROBLEMAS DE BANCO DE DADOS

### Verificar conexao:
```bash
docker-compose exec postgres pg_isready -U admin
```

### Verificar modelos:
```bash
ls -la backend/app/models/
grep -r "class.*Model" backend/app/models/
```

### Verificar schemas:
```bash
ls -la backend/app/schemas/
grep -r "class.*Schema" backend/app/schemas/
```

## 🖥️ PROBLEMAS DE FRONTEND

### Verificar componentes:
```bash
ls -la frontend/src/components/
ls -la frontend/src/pages/
```

### Verificar servicos de API:
```bash
grep -r "axios\|fetch\|api" frontend/src/services/
```

### Verificar tipos TypeScript:
```bash
ls -la frontend/src/types/
grep -r "interface\|type" frontend/src/types/
```

## 🔧 PROBLEMAS DE DOCKER

### Verificar status dos containers:
```bash
docker-compose ps
docker-compose logs --tail=50
```

### Verificar portas:
```bash
netstat -an | findstr "8000\|4000\|5432"
```

### Verificar volumes:
```bash
docker volume ls
docker-compose exec postgres ls -la /var/lib/postgresql/data/
```

## 📝 PROBLEMAS DE CONFIGURACAO

### Verificar variaveis de ambiente:
```bash
cat env.example
grep -r "config\|setting" backend/app/core/
```

### Verificar logs:
```bash
ls -la backend/logs/
tail -f backend/logs/app.log
```

### Verificar nginx:
```bash
docker-compose exec nginx nginx -t
cat nginx/nginx.conf
```

## 🚀 COMANDOS DE DIAGNOSTICO RAPIDO

### Sistema de Saude Geral:
```bash
# Verificar todos os servicos
docker-compose ps

# Verificar logs de erro
docker-compose logs | grep -i "error\|exception\|failed"

# Verificar conectividade
curl -s http://localhost:8000/health || echo "Backend offline"
curl -s http://localhost:4000 || echo "Frontend offline"
```

### Banco de Dados:
```bash
# Testar conexao
docker-compose exec postgres psql -U admin -d sistema_bi -c "SELECT 1;"

# Verificar tabelas
docker-compose exec postgres psql -U admin -d sistema_bi -c "\dt"

# Verificar usuarios
docker-compose exec postgres psql -U admin -d sistema_bi -c "SELECT * FROM users LIMIT 5;"
```

### API:
```bash
# Verificar documentacao
curl -s http://localhost:8000/docs || echo "API docs offline"

# Verificar endpoints
curl -s http://localhost:8000/api/v1/ || echo "API v1 offline"
```

## 🎯 FLUXO DE DIAGNOSTICO

### 1. Problema Reportado
- Identificar area (auth, upload, report, database, frontend)
- Usar palavras-chave apropriadas

### 2. Busca Direcionada
- Usar comandos de busca especificos
- Verificar arquivos relacionados
- Analisar logs relevantes

### 3. Diagnostico
- Executar comandos de verificacao
- Identificar causa raiz
- Aplicar solucao

### 4. Verificacao
- Testar solucao
- Verificar logs
- Confirmar funcionamento

## 📋 CHECKLIST DE VERIFICACAO

### Antes de Fazer Qualquer Busca:
- [ ] Identificar area do problema
- [ ] Escolher palavras-chave apropriadas
- [ ] Usar comandos direcionados
- [ ] Evitar full scan desnecessario

### Apos Identificar Problema:
- [ ] Verificar logs especificos
- [ ] Analisar arquivos relacionados
- [ ] Testar solucao
- [ ] Documentar resolucao

## 🔍 EXEMPLOS DE USO

### Problema: "Usuario nao consegue fazer login"
```bash
# 1. Verificar logs de autenticacao
docker-compose logs backend | grep -i "login\|auth"

# 2. Verificar endpoint de auth
grep -r "login" backend/app/api/v1/endpoints/auth.py

# 3. Verificar frontend
grep -r "login" frontend/src/pages/LoginPage.tsx
```

### Problema: "Relatorio nao gera PDF"
```bash
# 1. Verificar dependencias
grep -r "pdf\|reportlab" backend/requirements.txt

# 2. Verificar logs de relatorio
docker-compose logs backend | grep -i "report\|pdf"

# 3. Verificar endpoint
grep -r "pdf" backend/app/api/v1/endpoints/reports.py
```

### Problema: "Upload de arquivo falha"
```bash
# 1. Verificar permissoes
ls -la backend/uploads/

# 2. Verificar configuracoes
grep -r "upload\|file" backend/app/core/

# 3. Verificar logs
docker-compose logs backend | grep -i "upload\|file"
```
