// Tipos de usuario
export interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  full_name: string;
  role: string;
  permissions: string[];
  is_active: boolean;
  is_superuser: boolean;
  last_login?: string;
  created_at: string;
  updated_at?: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  role: string;
  permissions: string[];
  is_active: boolean;
}

export interface UserUpdate {
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  role?: string;
  permissions?: string[];
  is_active?: boolean;
  password?: string;
}

// Tipos de projeto
export interface Project {
  id: string;
  name: string;
  description?: string;
  status: string;
  priority: string;
  start_date?: string;
  end_date?: string;
  budget?: string;
  client_name?: string;
  is_active: boolean;
  created_by: string;
  created_by_user?: User;
  requirements_count: number;
  completed_requirements_count: number;
  progress_percentage: number;
  created_at: string;
  updated_at?: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status: string;
  priority: string;
  start_date?: string;
  end_date?: string;
  budget?: string;
  client_name?: string;
  is_active: boolean;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  status?: string;
  priority?: string;
  start_date?: string;
  end_date?: string;
  budget?: string;
  client_name?: string;
  is_active?: boolean;
}

// Tipos de requisito
export interface Requirement {
  id: string;
  title: string;
  description?: string;
  type: string;
  priority: string;
  status: string;
  complexity?: string;
  estimated_hours?: string;
  actual_hours?: string;
  due_date?: string;
  completion_date?: string;
  dynamic_fields: Record<string, any>;
  project_id: string;
  project?: Project;
  assigned_to?: string;
  assigned_user?: User;
  created_by: string;
  created_by_user?: User;
  is_overdue: boolean;
  days_until_due?: number;
  progress_percentage: number;
  created_at: string;
  updated_at?: string;
}

export interface RequirementCreate {
  title: string;
  description?: string;
  type: string;
  priority: string;
  status: string;
  complexity?: string;
  estimated_hours?: string;
  actual_hours?: string;
  due_date?: string;
  completion_date?: string;
  dynamic_fields: Record<string, any>;
  project_id: string;
  assigned_to?: string;
}

export interface RequirementUpdate {
  title?: string;
  description?: string;
  type?: string;
  priority?: string;
  status?: string;
  complexity?: string;
  estimated_hours?: string;
  actual_hours?: string;
  due_date?: string;
  completion_date?: string;
  assigned_to?: string;
  dynamic_fields?: Record<string, any>;
}

// Tipos de campo dinamico
export interface DynamicField {
  id: string;
  field_name: string;
  field_type: string;
  field_label?: string;
  field_description?: string;
  options?: string[];
  is_required: boolean;
  is_active: boolean;
  applies_to: string;
  order_index?: string;
  validation_rules?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface DynamicFieldCreate {
  field_name: string;
  field_type: string;
  field_label?: string;
  field_description?: string;
  options?: string[];
  is_required: boolean;
  is_active: boolean;
  applies_to: string;
  order_index?: string;
  validation_rules?: Record<string, any>;
}

export interface DynamicFieldUpdate {
  field_name?: string;
  field_type?: string;
  field_label?: string;
  field_description?: string;
  options?: string[];
  is_required?: boolean;
  is_active?: boolean;
  applies_to?: string;
  order_index?: string;
  validation_rules?: Record<string, any>;
}

// Tipos de autenticacao
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface TokenData {
  username?: string;
  user_id?: string;
}

// Tipos de relatorio
export interface DashboardData {
  summary: {
    total_projects: number;
    active_projects: number;
    total_requirements: number;
    completed_requirements: number;
    overdue_requirements: number;
    recent_projects: number;
    recent_requirements: number;
  };
  projects_by_status: Array<{ status: string; count: number }>;
  requirements_by_status: Array<{ status: string; count: number }>;
  requirements_by_type: Array<{ type: string; count: number }>;
  requirements_by_priority: Array<{ priority: string; count: number }>;
}

export interface ProjectSummary {
  project: {
    id: string;
    name: string;
    description?: string;
    status: string;
    priority: string;
    client_name?: string;
    progress_percentage: number;
  };
  statistics: {
    total_requirements: number;
    completed_requirements: number;
    overdue_requirements: number;
    completion_rate: number;
  };
  requirements_by_status: Array<{ status: string; count: number }>;
  requirements_by_type: Array<{ type: string; count: number }>;
  requirements_by_priority: Array<{ priority: string; count: number }>;
}

// Tipos de filtros
export interface ProjectFilter {
  status?: string;
  priority?: string;
  client_name?: string;
  created_by?: string;
  is_active?: boolean;
  search?: string;
}

export interface RequirementFilter {
  project_id?: string;
  type?: string;
  priority?: string;
  status?: string;
  complexity?: string;
  assigned_to?: string;
  created_by?: string;
  is_overdue?: boolean;
  search?: string;
}

// Tipos de resposta da API
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Enums
export enum ProjectStatus {
  EM_ANDAMENTO = 'em_andamento',
  CONCLUIDO = 'concluido',
  CANCELADO = 'cancelado',
  PAUSADO = 'pausado',
}

export enum ProjectPriority {
  BAIXA = 'baixa',
  MEDIA = 'media',
  ALTA = 'alta',
  CRITICA = 'critica',
}

export enum RequirementType {
  FUNCIONAL = 'funcional',
  NAO_FUNCIONAL = 'nao_funcional',
  REGRA_NEGOCIO = 'regra_negocio',
}

export enum RequirementStatus {
  PENDENTE = 'pendente',
  EM_ANALISE = 'em_analise',
  APROVADO = 'aprovado',
  EM_DESENVOLVIMENTO = 'em_desenvolvimento',
  CONCLUIDO = 'concluido',
  CANCELADO = 'cancelado',
}

export enum RequirementPriority {
  BAIXA = 'baixa',
  MEDIA = 'media',
  ALTA = 'alta',
  CRITICA = 'critica',
}

export enum RequirementComplexity {
  BAIXA = 'baixa',
  MEDIA = 'media',
  ALTA = 'alta',
}

export enum UserRole {
  ADMIN = 'admin',
  GERENTE = 'gerente',
  ANALISTA = 'analista',
  DESENVOLVEDOR = 'desenvolvedor',
}

export enum FieldType {
  TEXT = 'text',
  NUMBER = 'number',
  DATE = 'date',
  SELECT = 'select',
  TEXTAREA = 'textarea',
  BOOLEAN = 'boolean',
}
