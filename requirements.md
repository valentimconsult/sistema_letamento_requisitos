
# Requisitos do Sistema de Levantamento de Requisitos de BI

## Requisitos Funcionais:

1.  **Gestão de Projetos:**
    *   Criar, visualizar, editar e excluir projetos de BI.
    *   Associar requisitos a projetos específicos.
    *   Definir status para cada projeto (Ex: Em andamento, Concluído, Cancelado).

2.  **Gestão de Requisitos:**
    *   Criar, visualizar, editar e excluir requisitos para cada projeto.
    *   Definir tipo de requisito (Ex: Funcional, Não Funcional, Regra de Negócio).
    *   Definir prioridade do requisito (Ex: Alta, Média, Baixa).
    *   Definir status do requisito (Ex: Pendente, Em Análise, Aprovado, Em Desenvolvimento, Concluído).
    *   Associar requisitos a usuários/stakeholders.

3.  **Campos Dinâmicos para Descrição de Requisitos:**
    *   Capacidade de adicionar campos personalizados (texto, número, data, seleção, etc.) para detalhar os requisitos.
    *   Configuração desses campos por tipo de projeto ou globalmente.
    *   Validação de dados para os campos dinâmicos.

4.  **Pesquisa e Filtragem:**
    *   Pesquisar projetos e requisitos por palavras-chave.
    *   Filtrar projetos e requisitos por status, tipo, prioridade, etc.

5.  **Autenticação e Autorização:**
    *   Sistema de login/logout para usuários.
    *   Diferentes níveis de acesso (Ex: Administrador, Gerente de Projeto, Analista).
    *   Permissões baseadas em funções para criação, edição e visualização de dados.

6.  **Relatórios Básicos:**
    *   Visualização de um resumo de projetos e requisitos.
    *   Exportação de dados de projetos e requisitos (Ex: CSV, PDF).

## Requisitos Não Funcionais:

1.  **Usabilidade:**
    *   Interface de usuário intuitiva e fácil de usar.
    *   Design responsivo para acesso em diferentes dispositivos (desktop, tablet, mobile).

2.  **Desempenho:**
    *   Tempos de resposta rápidos para operações comuns (criação, edição, pesquisa).
    *   Capacidade de lidar com um número crescente de projetos e requisitos sem degradação significativa de desempenho.

3.  **Segurança:**
    *   Proteção contra acesso não autorizado (autenticação e autorização robustas).
    *   Proteção contra injeção de SQL, XSS e outras vulnerabilidades comuns.
    *   Criptografia de senhas de usuários.

4.  **Confiabilidade:**
    *   Disponibilidade do sistema (uptime).
    *   Mecanismos de backup e recuperação de dados.

5.  **Manutenibilidade:**
    *   Código bem estruturado e documentado.
    *   Fácil de atualizar e estender com novas funcionalidades.

6.  **Escalabilidade:**
    *   Capacidade de escalar horizontalmente (adicionar mais servidores) e verticalmente (aumentar recursos de um servidor) conforme a demanda.

7.  **Compatibilidade:**
    *   Compatibilidade com navegadores modernos (Chrome, Firefox, Edge, Safari).

8.  **Flexibilidade:**
    *   Facilidade para adicionar novos tipos de campos dinâmicos no futuro.
    *   Possibilidade de integração com outras ferramentas (futuramente).


