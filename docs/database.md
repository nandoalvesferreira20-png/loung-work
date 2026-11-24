# Modelo proposto para o PostgreSQL

A Fase 0 prepara metadados SQLAlchemy e Alembic. A primeira revisão de schema acompanhará a primeira funcionalidade persistida.

| Tabela             | Relações e índices propostos                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------- |
| candidate_profiles | PK UUID referencia auth.users.id e define o proprietário                                      |
| candidate_skills   | FK de perfil e unicidade por perfil e habilidade normalizada                                  |
| work_experiences   | FK de perfil e índice em perfil e data de início                                              |
| educations         | FK de perfil e índice em perfil e data de início                                              |
| resumes            | FK de perfil e índice em perfil e atualização                                                 |
| resume_versions    | FK de currículo e unicidade por currículo e versão                                            |
| job_sources        | Chave única por fonte autorizada                                                              |
| jobs               | FK de fonte, unicidade com identificador externo e índice em published_at e id para paginação |
| saved_jobs         | PK composta por perfil e vaga e índice em job_id                                              |
| job_matches        | FKs de versão e vaga e unicidade por versão, vaga e versão do algoritmo                       |
| applications       | FKs de perfil e vaga e índice em perfil, status e atualização                                 |

Ative RLS junto de cada tabela exposta. Para leitura e escrita privadas, use `auth.uid()` e verifique propriedade tanto em USING quanto em WITH CHECK conforme a operação. Para versões e análises, verifique o proprietário pelo currículo. Para vagas, exponha apenas registros publicados. Restrinja ingestão e administração de fontes a papéis internos.

Conexões SQLAlchemy diretas não recebem claims do Supabase automaticamente. Antes de abrir rotas persistentes, aplique filtros por UUID validado no repositório e teste acesso entre usuários. Se adotar RLS via conexão direta, use papel sem BYPASSRLS e configure o contexto de usuário por transação. Reserve o papel privilegiado para migrations.

Armazene currículos em bucket privado com políticas em storage.objects ligadas ao proprietário. Use URLs assinadas de curta duração quando necessárias. Defina retenção e exclusão dos arquivos, versões, análises e dados do perfil. Registre a finalidade do tratamento e evite dados de currículo em logs.
