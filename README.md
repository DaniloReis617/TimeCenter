###Estrutura Recomendada do Projeto###
TimeCenter/app/
├── app.py: Arquivo principal do aplicativo, gerencia a navegação, autenticação, e implementa controle de acesso por perfil (Super Usuário, Administrador, Gestor, Visualizador).
├── utils.py: Funções utilitárias, como conexões de banco de dados, validações e operações CRUD (ler, criar, atualizar, deletar dados).
├── README.ME: Anotações e descrição da estrutura do app, incluindo orientações de uso.
├── imagens/: Pasta que contém as imagens utilizadas no app, como logos e ícones.
├── .streamlit/
│ ├── config.toml: Configurações de tema e servidor para o Streamlit.
│ └── secrets.toml: Segredos do banco de dados, como credenciais de acesso.
└── pages/
├── screens.py: Contém as telas utilizadas no aplicativo, como home, stakeholders, escopo, custos, administração, etc.

Atualizações Recentes:
Controle de Acesso: Implementado no app.py, controlando o acesso às telas com base no perfil do usuário.
Super Usuário: Acesso total.
Administrador: Acesso total, exceto funções exclusivas de Super Usuário.
Gestor: Acesso às telas de gerenciamento de projetos.
Visualizador: Acesso às telas de visualização.
Tela de Administração (adm_screen): Permite a exibição, cadastro e edição de usuários na tabela timecenter.TB_USUARIO. Inclui:
Dashboard de Usuários: Exibe informações como login, status e nível de acesso.
Cadastro de Novos Usuários: Permite adicionar novos usuários.
Edição de Usuários: Permite editar informações de usuários existentes.