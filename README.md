# Pill Alarm

O **Pill Alarm** é uma aplicação backend construída para auxiliar no controle de rotinas de medicação. O sistema gerencia usuários, cadastros de remédios, horários programados (schedules) e logs de histórico de consumo.

<p align="left">
  <img src="https://img.shields.io/badge/Em%20Desenvolvimento-yellow?style=for-the-badge">
</p>

---



---

## Arquitetura do Projeto

A estrutura de pastas do projeto foi organizada da seguinte forma:

```text
pill-alarm/
│
├── app/                  # núcleo da aplicação
│   ├── models/           # modelos de dados do SQLAlchemy
│   ├── routes/           # rotas e blueprints da api
│   ├── services/         # regras de negócios
│   └── __init__.py       # inicialização do app
│
├── database/             # script sql
│   └── schema.sql        # 
│
├── migrations/           # migrações de banco de dados
├── venv/                 # ambiente virtual Python
├── .env.example          # exemplo de variáveis de ambiente
├── .gitignore            
├── config.py             
├── requirements.txt      
└── run.py                # ponto de entrada da aplicação