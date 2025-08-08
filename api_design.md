
# Design da API RESTful

Esta seção detalha os endpoints da API RESTful para o sistema de levantamento de requisitos de BI, incluindo métodos HTTP, URLs, formatos de requisição e resposta.

## 1. Autenticação

### `POST /api/auth/register`
*   **Descrição:** Registra um novo usuário.
*   **Requisição:**
    ```json
    {
      "username": "novo_usuario",
      "email": "email@example.com",
      "password": "senha_segura"
    }
    ```
*   **Resposta (Sucesso - 201 Created):**
    ```json
    {
      "message": "Usuário registrado com sucesso",
      "user_id": "<uuid_do_usuario>"
    }
    ```
*   **Resposta (Erro - 400 Bad Request):**
    ```json
    {
      "message": "Nome de usuário ou e-mail já em uso"
    }
    ```

### `POST /api/auth/login`
*   **Descrição:** Autentica um usuário e retorna um token de acesso.
*   **Requisição:**
    ```json
    {
      "username": "usuario_existente",
      "password": "senha_do_usuario"
    }
    ```
*   **Resposta (Sucesso - 200 OK):**
    ```json
    {
      "access_token": "<jwt_token>",
      "token_type": "bearer"
    }
    ```
*   **Resposta (Erro - 401 Unauthorized):**
    ```json
    {
      "message": "Credenciais inválidas"
    }
    ```

## 2. Projetos (`/api/projects`)

### `GET /api/projects`
*   **Descrição:** Lista todos os projetos.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 200 OK):**
    ```json
    [
      {
        "id": "<uuid_do_projeto_1>",
        "name": "Projeto BI Vendas",
        "description": "Análise de vendas do último ano",
        "status": "Em Andamento",
        "created_at": "2025-01-15T10:00:00Z",
        "updated_at": "2025-01-15T10:00:00Z"
      },
      // ... outros projetos
    ]
    ```

### `GET /api/projects/<project_id>`
*   **Descrição:** Obtém detalhes de um projeto específico.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 200 OK):**
    ```json
    {
      "id": "<uuid_do_projeto>",
      "name": "Projeto BI Vendas",
      "description": "Análise de vendas do último ano",
      "status": "Em Andamento",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
    ```
*   **Resposta (Erro - 404 Not Found):**
    ```json
    {
      "message": "Projeto não encontrado"
    }
    ```

### `POST /api/projects`
*   **Descrição:** Cria um novo projeto.
*   **Requisição:**
    ```json
    {
      "name": "Novo Projeto BI",
      "description": "Descrição do novo projeto",
      "status": "Em Andamento"
    }
    ```
*   **Resposta (Sucesso - 201 Created):**
    ```json
    {
      "id": "<uuid_do_novo_projeto>",
      "name": "Novo Projeto BI",
      "description": "Descrição do novo projeto",
      "status": "Em Andamento",
      "created_at": "2025-07-09T14:30:00Z",
      "updated_at": "2025-07-09T14:30:00Z"
    }
    ```
*   **Resposta (Erro - 400 Bad Request):**
    ```json
    {
      "message": "Dados inválidos para o projeto"
    }
    ```

### `PUT /api/projects/<project_id>`
*   **Descrição:** Atualiza um projeto existente.
*   **Requisição:**
    ```json
    {
      "name": "Projeto BI Vendas Atualizado",
      "description": "Análise de vendas do último ano e projeções",
      "status": "Concluído"
    }
    ```
*   **Resposta (Sucesso - 200 OK):**
    ```json
    {
      "id": "<uuid_do_projeto>",
      "name": "Projeto BI Vendas Atualizado",
      "description": "Análise de vendas do último ano e projeções",
      "status": "Concluído",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-07-09T14:45:00Z"
    }
    ```
*   **Resposta (Erro - 404 Not Found ou 400 Bad Request):**
    ```json
    {
      "message": "Projeto não encontrado" ou "Dados inválidos"
    }
    ```

### `DELETE /api/projects/<project_id>`
*   **Descrição:** Exclui um projeto.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 204 No Content):** N/A
*   **Resposta (Erro - 404 Not Found):**
    ```json
    {
      "message": "Projeto não encontrado"
    }
    ```

## 3. Requisitos (`/api/projects/<project_id>/requirements`)

### `GET /api/projects/<project_id>/requirements`
*   **Descrição:** Lista todos os requisitos de um projeto específico.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 200 OK):**
    ```json
    [
      {
        "id": "<uuid_do_requisito_1>",
        "project_id": "<uuid_do_projeto>",
        "title": "Requisito de Dashboard de Vendas",
        "description": "Criar dashboard interativo para vendas",
        "type": "Funcional",
        "priority": "Alta",
        "status": "Em Desenvolvimento",
        "assigned_to": "<uuid_do_usuario>",
        "dynamic_fields": {
          "Fonte de Dados": "Sistema ERP",
          "KPIs Envolvidos": ["Vendas", "Lucratividade"]
        },
        "created_at": "2025-02-01T09:00:00Z",
        "updated_at": "2025-02-01T09:00:00Z"
      },
      // ... outros requisitos
    ]
    ```

### `GET /api/requirements/<requirement_id>`
*   **Descrição:** Obtém detalhes de um requisito específico (acesso direto).
*   **Requisição:** N/A
*   **Resposta (Sucesso - 200 OK):**
    ```json
    {
      "id": "<uuid_do_requisito>",
      "project_id": "<uuid_do_projeto>",
      "title": "Requisito de Dashboard de Vendas",
      "description": "Criar dashboard interativo para vendas",
      "type": "Funcional",
      "priority": "Alta",
      "status": "Em Desenvolvimento",
      "assigned_to": "<uuid_do_usuario>",
      "dynamic_fields": {
        "Fonte de Dados": "Sistema ERP",
        "KPIs Envolvidos": ["Vendas", "Lucratividade"]
      },
      "created_at": "2025-02-01T09:00:00Z",
      "updated_at": "2025-02-01T09:00:00Z"
    }
    ```
*   **Resposta (Erro - 404 Not Found):**
    ```json
    {
      "message": "Requisito não encontrado"
    }
    ```

### `POST /api/projects/<project_id>/requirements`
*   **Descrição:** Cria um novo requisito para um projeto.
*   **Requisição:**
    ```json
    {
      "title": "Novo Requisito",
      "description": "Descrição do novo requisito",
      "type": "Não Funcional",
      "priority": "Média",
      "status": "Pendente",
      "assigned_to": "<uuid_do_usuario>",
      "dynamic_fields": {
        "Impacto": "Alto",
        "Observacoes": "Depende da integração X"
      }
    }
    ```
*   **Resposta (Sucesso - 201 Created):**
    ```json
    {
      "id": "<uuid_do_novo_requisito>",
      "project_id": "<uuid_do_projeto>",
      "title": "Novo Requisito",
      "description": "Descrição do novo requisito",
      "type": "Não Funcional",
      "priority": "Média",
      "status": "Pendente",
      "assigned_to": "<uuid_do_usuario>",
      "dynamic_fields": {
        "Impacto": "Alto",
        "Observacoes": "Depende da integração X"
      },
      "created_at": "2025-07-09T15:00:00Z",
      "updated_at": "2025-07-09T15:00:00Z"
    }
    ```
*   **Resposta (Erro - 400 Bad Request ou 404 Not Found):**
    ```json
    {
      "message": "Dados inválidos para o requisito" ou "Projeto não encontrado"
    }
    ```

### `PUT /api/requirements/<requirement_id>`
*   **Descrição:** Atualiza um requisito existente.
*   **Requisição:**
    ```json
    {
      "title": "Requisito Atualizado",
      "description": "Descrição atualizada do requisito",
      "status": "Aprovado",
      "dynamic_fields": {
        "Impacto": "Baixo",
        "Observacoes": "Integrado com sucesso"
      }
    }
    ```
*   **Resposta (Sucesso - 200 OK):**
    ```json
    {
      "id": "<uuid_do_requisito>",
      "project_id": "<uuid_do_projeto>",
      "title": "Requisito Atualizado",
      "description": "Descrição atualizada do requisito",
      "type": "Não Funcional",
      "priority": "Média",
      "status": "Aprovado",
      "assigned_to": "<uuid_do_usuario>",
      "dynamic_fields": {
        "Impacto": "Baixo",
        "Observacoes": "Integrado com sucesso"
      },
      "created_at": "2025-02-01T09:00:00Z",
      "updated_at": "2025-07-09T15:15:00Z"
    }
    ```
*   **Resposta (Erro - 404 Not Found ou 400 Bad Request):**
    ```json
    {
      "message": "Requisito não encontrado" ou "Dados inválidos"
    }
    ```

### `DELETE /api/requirements/<requirement_id>`
*   **Descrição:** Exclui um requisito.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 204 No Content):** N/A
*   **Resposta (Erro - 404 Not Found):**
    ```json
    {
      "message": "Requisito não encontrado"
    }
    ```

## 4. Definições de Campos Dinâmicos (`/api/dynamic-fields`)

### `GET /api/dynamic-fields`
*   **Descrição:** Lista todas as definições de campos dinâmicos.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 200 OK):**
    ```json
    [
      {
        "id": "<uuid_da_definicao_1>",
        "field_name": "Fonte de Dados",
        "field_type": "text",
        "options": null,
        "is_required": false,
        "applies_to": "requirement",
        "created_at": "2025-03-01T11:00:00Z",
        "updated_at": "2025-03-01T11:00:00Z"
      },
      {
        "id": "<uuid_da_definicao_2>",
        "field_name": "KPIs Envolvidos",
        "field_type": "select",
        "options": ["Vendas", "Lucratividade", "Custo"],
        "is_required": true,
        "applies_to": "requirement",
        "created_at": "2025-03-01T11:05:00Z",
        "updated_at": "2025-03-01T11:05:00Z"
      }
      // ... outras definições
    ]
    ```

### `POST /api/dynamic-fields`
*   **Descrição:** Cria uma nova definição de campo dinâmico.
*   **Requisição:**
    ```json
    {
      "field_name": "Data de Entrega Estimada",
      "field_type": "date",
      "options": null,
      "is_required": false,
      "applies_to": "requirement"
    }
    ```
*   **Resposta (Sucesso - 201 Created):**
    ```json
    {
      "id": "<uuid_da_nova_definicao>",
      "field_name": "Data de Entrega Estimada",
      "field_type": "date",
      "options": null,
      "is_required": false,
      "applies_to": "requirement",
      "created_at": "2025-07-09T15:30:00Z",
      "updated_at": "2025-07-09T15:30:00Z"
    }
    ```
*   **Resposta (Erro - 400 Bad Request):**
    ```json
    {
      "message": "Dados inválidos para a definição do campo"
    }
    ```

### `PUT /api/dynamic-fields/<field_id>`
*   **Descrição:** Atualiza uma definição de campo dinâmico existente.
*   **Requisição:**
    ```json
    {
      "field_name": "Data de Entrega Final",
      "field_type": "date",
      "is_required": true
    }
    ```
*   **Resposta (Sucesso - 200 OK):**
    ```json
    {
      "id": "<uuid_da_definicao>",
      "field_name": "Data de Entrega Final",
      "field_type": "date",
      "options": null,
      "is_required": true,
      "applies_to": "requirement",
      "created_at": "2025-03-01T11:00:00Z",
      "updated_at": "2025-07-09T15:45:00Z"
    }
    ```
*   **Resposta (Erro - 404 Not Found ou 400 Bad Request):**
    ```json
    {
      "message": "Definição de campo não encontrada" ou "Dados inválidos"
    }
    ```

### `DELETE /api/dynamic-fields/<field_id>`
*   **Descrição:** Exclui uma definição de campo dinâmico.
*   **Requisição:** N/A
*   **Resposta (Sucesso - 204 No Content):** N/A
*   **Resposta (Erro - 404 Not Found):**
    ```json
    {
      "message": "Definição de campo não encontrada"
    }
    ```


