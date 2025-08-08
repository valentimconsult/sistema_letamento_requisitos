# Modelo de Dados

## 1. Tabela `projects`
Armazena informações sobre os projetos de BI.

| Coluna        | Tipo         | Descrição                                   |
|---------------|--------------|---------------------------------------------|
| `id`          | UUID/Integer | Chave primária, identificador único do projeto |
| `name`        | VARCHAR(255) | Nome do projeto                             |
| `description` | TEXT         | Descrição detalhada do projeto              |
| `status`      | VARCHAR(50)  | Status atual do projeto (Ex: 'Em Andamento', 'Concluído') |
| `created_at`  | TIMESTAMP    | Data e hora de criação do projeto           |
| `updated_at`  | TIMESTAMP    | Data e hora da última atualização do projeto |

## 2. Tabela `requirements`
Armazena informações sobre os requisitos de cada projeto.

| Coluna          | Tipo         | Descrição                                   |
|-----------------|--------------|---------------------------------------------|
| `id`            | UUID/Integer | Chave primária, identificador único do requisito |
| `project_id`    | UUID/Integer | Chave estrangeira para `projects.id`        |
| `title`         | VARCHAR(255) | Título/nome do requisito                    |
| `description`   | TEXT         | Descrição básica do requisito               |
| `type`          | VARCHAR(50)  | Tipo de requisito (Ex: 'Funcional', 'Não Funcional') |
| `priority`      | VARCHAR(50)  | Prioridade do requisito (Ex: 'Alta', 'Média') |
| `status`        | VARCHAR(50)  | Status atual do requisito (Ex: 'Pendente', 'Aprovado') |
| `assigned_to`   | UUID/Integer | Chave estrangeira para `users.id` (se houver gestão de usuários) |
| `dynamic_fields`| JSONB        | Armazena dados dos campos dinâmicos em formato JSON |
| `created_at`    | TIMESTAMP    | Data e hora de criação do requisito         |
| `updated_at`    | TIMESTAMP    | Data e hora da última atualização do requisito |

## 3. Tabela `users` (Opcional, se houver gestão de usuários)
Armazena informações sobre os usuários do sistema.

| Coluna        | Tipo         | Descrição                                   |
|---------------|--------------|---------------------------------------------|
| `id`          | UUID/Integer | Chave primária, identificador único do usuário |
| `username`    | VARCHAR(255) | Nome de usuário                             |
| `email`       | VARCHAR(255) | Endereço de e-mail do usuário               |
| `password_hash`| VARCHAR(255) | Hash da senha do usuário                    |
| `role`        | VARCHAR(50)  | Papel/nível de acesso do usuário (Ex: 'admin', 'project_manager') |
| `created_at`  | TIMESTAMP    | Data e hora de criação do usuário           |
| `updated_at`  | TIMESTAMP    | Data e hora da última atualização do usuário |

## 4. Tabela `dynamic_field_definitions`
Armazena as definições dos campos dinâmicos que podem ser associados a requisitos ou projetos.

| Coluna        | Tipo         | Descrição                                   |
|---------------|--------------|---------------------------------------------|
| `id`          | UUID/Integer | Chave primária, identificador único da definição do campo |
| `field_name`  | VARCHAR(255) | Nome do campo (Ex: 'Fonte de Dados', 'KPIs Envolvidos') |
| `field_type`  | VARCHAR(50)  | Tipo de dado do campo (Ex: 'text', 'number', 'date', 'select') |
| `options`     | JSONB        | Opções para campos do tipo 'select' (array de strings) |
| `is_required` | BOOLEAN      | Indica se o campo é obrigatório             |
| `applies_to`  | VARCHAR(50)  | Onde o campo se aplica (Ex: 'requirement', 'project', 'global') |
| `created_at`  | TIMESTAMP    | Data e hora de criação da definição do campo |
| `updated_at`  | TIMESTAMP    | Data e hora da última atualização da definição do campo |

## Relacionamentos:
*   `projects.id` (1) <--- (N) `requirements.project_id`
*   `users.id` (1) <--- (N) `requirements.assigned_to` (Opcional)

## Observações sobre `dynamic_fields` na tabela `requirements`:
O campo `dynamic_fields` será do tipo `JSONB` no PostgreSQL. Isso permite armazenar um objeto JSON flexível onde as chaves são os `field_name` das definições de campos dinâmicos e os valores são os dados inseridos pelo usuário para aquele requisito específico. Exemplo:

```json
{
  "Fonte de Dados": "Sistema ERP",
  "KPIs Envolvidos": ["Vendas", "Lucratividade"],
  "Data de Entrega Estimada": "2025-12-31"
}
```


