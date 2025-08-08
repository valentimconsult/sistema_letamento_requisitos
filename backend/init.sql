-- Script de inicializacao do banco de dados PostgreSQL
-- Sistema BI - Levantamento de Requisitos

-- Criar extensoes necessarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar tabela de usuarios
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    permissions JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Criar tabela de projetos
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'em_andamento',
    priority VARCHAR(50) NOT NULL DEFAULT 'media',
    start_date DATE,
    end_date DATE,
    budget VARCHAR(100),
    client_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Criar tabela de definicoes de campos dinamicos
CREATE TABLE IF NOT EXISTS dynamic_field_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_name VARCHAR(100) NOT NULL,
    field_type VARCHAR(50) NOT NULL,
    field_label VARCHAR(255),
    field_description TEXT,
    options JSONB,
    is_required BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    applies_to VARCHAR(50) NOT NULL,
    order_index VARCHAR(10),
    validation_rules JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(field_name, applies_to)
);

-- Criar tabela de requisitos
CREATE TABLE IF NOT EXISTS requirements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL DEFAULT 'funcional',
    priority VARCHAR(50) NOT NULL DEFAULT 'media',
    status VARCHAR(50) NOT NULL DEFAULT 'pendente',
    complexity VARCHAR(50),
    estimated_hours VARCHAR(10),
    actual_hours VARCHAR(10),
    due_date DATE,
    completion_date DATE,
    dynamic_fields JSONB DEFAULT '{}',
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    assigned_to UUID REFERENCES users(id),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Criar indices para melhor performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_created_by ON projects(created_by);
CREATE INDEX IF NOT EXISTS idx_requirements_project_id ON requirements(project_id);
CREATE INDEX IF NOT EXISTS idx_requirements_status ON requirements(status);
CREATE INDEX IF NOT EXISTS idx_requirements_assigned_to ON requirements(assigned_to);
CREATE INDEX IF NOT EXISTS idx_dynamic_fields_applies_to ON dynamic_field_definitions(applies_to);

-- Criar usuario administrador padrao
-- Senha: admin123 (hash bcrypt)
INSERT INTO users (id, username, email, password_hash, first_name, last_name, role, permissions, is_active, is_superuser, created_at, updated_at)
VALUES (
    uuid_generate_v4(),
    'admin',
    'admin@sistema-bi.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPDwKqKqK',
    'Administrador',
    'Sistema',
    'admin',
    '["user:read", "user:create", "user:update", "user:delete", "user:admin", "project:read", "project:create", "project:update", "project:delete", "project:admin", "requirement:read", "requirement:create", "requirement:update", "requirement:delete", "requirement:admin", "dynamic_field:read", "dynamic_field:create", "dynamic_field:update", "dynamic_field:delete", "report:read", "report:export"]',
    true,
    true,
    NOW(),
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Criar usuario analista padrao
-- Senha: analista123 (hash bcrypt)
INSERT INTO users (id, username, email, password_hash, first_name, last_name, role, permissions, is_active, is_superuser, created_at, updated_at)
VALUES (
    uuid_generate_v4(),
    'analista',
    'analista@sistema-bi.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPDwKqKqK',
    'Analista',
    'BI',
    'analista',
    '["project:read", "project:create", "project:update", "requirement:read", "requirement:create", "requirement:update", "dynamic_field:read", "report:read"]',
    true,
    false,
    NOW(),
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Criar campos dinamicos padrao
INSERT INTO dynamic_field_definitions (id, field_name, field_type, field_label, field_description, options, is_required, is_active, applies_to, order_index, created_at, updated_at)
VALUES
    (uuid_generate_v4(), 'fonte_dados', 'text', 'Fonte de Dados', 'Sistema ou fonte de dados principal', NULL, false, true, 'requirement', '1', NOW(), NOW()),
    (uuid_generate_v4(), 'kpis_envolvidos', 'select', 'KPIs Envolvidos', 'Indicadores de performance relacionados', '["Vendas", "Lucratividade", "Custo", "ROI", "Produtividade"]', false, true, 'requirement', '2', NOW(), NOW()),
    (uuid_generate_v4(), 'data_entrega_estimada', 'date', 'Data de Entrega Estimada', 'Data estimada para entrega', NULL, false, true, 'requirement', '3', NOW(), NOW()),
    (uuid_generate_v4(), 'complexidade', 'select', 'Complexidade', 'Nivel de complexidade do requisito', '["Baixa", "Media", "Alta"]', false, true, 'requirement', '4', NOW(), NOW()),
    (uuid_generate_v4(), 'observacoes', 'textarea', 'Observacoes', 'Observacoes adicionais', NULL, false, true, 'requirement', '5', NOW(), NOW())
ON CONFLICT (field_name, applies_to) DO NOTHING;

-- Criar projeto de exemplo
INSERT INTO projects (id, name, description, status, priority, start_date, end_date, budget, client_name, is_active, created_by, created_at, updated_at)
VALUES (
    uuid_generate_v4(),
    'Projeto BI Vendas',
    'Sistema de Business Intelligence para analise de vendas',
    'em_andamento',
    'alta',
    NOW(),
    NOW() + INTERVAL '90 days',
    'R$ 50.000,00',
    'Empresa ABC Ltda',
    true,
    (SELECT id FROM users WHERE username = 'admin' LIMIT 1),
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Criar requisitos de exemplo
INSERT INTO requirements (id, title, description, type, priority, status, complexity, estimated_hours, due_date, dynamic_fields, project_id, assigned_to, created_by, created_at, updated_at)
VALUES
    (
        uuid_generate_v4(),
        'Dashboard de Vendas',
        'Criar dashboard interativo para visualizacao de vendas',
        'funcional',
        'alta',
        'em_desenvolvimento',
        'media',
        '40',
        NOW() + INTERVAL '30 days',
        '{"fonte_dados": "Sistema ERP", "kpis_envolvidos": ["Vendas", "Lucratividade"], "complexidade": "Media", "observacoes": "Integrar com sistema de vendas"}',
        (SELECT id FROM projects WHERE name = 'Projeto BI Vendas' LIMIT 1),
        (SELECT id FROM users WHERE username = 'analista' LIMIT 1),
        (SELECT id FROM users WHERE username = 'admin' LIMIT 1),
        NOW(),
        NOW()
    ),
    (
        uuid_generate_v4(),
        'Relatorio de Performance',
        'Gerar relatorios automaticos de performance',
        'funcional',
        'media',
        'pendente',
        'baixa',
        '20',
        NOW() + INTERVAL '45 days',
        '{"fonte_dados": "Sistema CRM", "kpis_envolvidos": ["ROI", "Produtividade"], "complexidade": "Baixa", "observacoes": "Relatorios semanais"}',
        (SELECT id FROM projects WHERE name = 'Projeto BI Vendas' LIMIT 1),
        (SELECT id FROM users WHERE username = 'analista' LIMIT 1),
        (SELECT id FROM users WHERE username = 'admin' LIMIT 1),
        NOW(),
        NOW()
    ),
    (
        uuid_generate_v4(),
        'Seguranca de Dados',
        'Implementar medidas de seguranca para protecao de dados',
        'nao_funcional',
        'critica',
        'em_analise',
        'alta',
        '60',
        NOW() + INTERVAL '60 days',
        '{"fonte_dados": "Sistema de Seguranca", "kpis_envolvidos": ["Custo"], "complexidade": "Alta", "observacoes": "Conformidade LGPD"}',
        (SELECT id FROM projects WHERE name = 'Projeto BI Vendas' LIMIT 1),
        (SELECT id FROM users WHERE username = 'admin' LIMIT 1),
        (SELECT id FROM users WHERE username = 'admin' LIMIT 1),
        NOW(),
        NOW()
    )
ON CONFLICT DO NOTHING;
