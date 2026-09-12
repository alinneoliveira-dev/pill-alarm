# Pill Alarm

O **Pill Alarm** é uma aplicação desenvolvida para auxiliar no controle de rotinas de medicação.

O sistema permite cadastrar usuários, medicamentos e horários programados, além de registrar o histórico das medicações como **tomadas** ou **não tomadas**.

A aplicação também utiliza automação para enviar lembretes pelo **Telegram** e processar a resposta do usuário em tempo real.

<p align="left">
<img src="https://img.shields.io/badge/Em%20Desenvolvimento-yellow?style=for-the-badge">
</p>

---

## Sobre o projeto

O projeto foi desenvolvido com foco em integração entre **API, banco de dados e automação**, utilizando Flask como backend, PostgreSQL para persistência dos dados e n8n para orquestração dos lembretes e respostas.

O fluxo permite:

- Cadastro de usuários
- Cadastro de medicamentos
- Cadastro de horários de medicação
- Geração de lembretes
- Envio de notificações pelo Telegram
- Registro da resposta do usuário
- Histórico de medicações tomadas ou não tomadas
- Prevenção de registros duplicados

---

## Tecnologias

- **Python**
- **Flask**
- **SQLAlchemy**
- **PostgreSQL**
- **n8n**
- **Telegram Bot API**
- **Docker**
- **HTML / CSS / JavaScript** *(em desenvolvimento)*

---

  <p align="center">
  <img src="app/docs/images/n8n_workflow1.png" width="410">
  <img src="app/docs/images/n8n_workflow2.png" width="400">
  </p>

---

## Arquitetura

```mermaid
flowchart LR
    A[(PostgreSQL)] --> B[Flask API]
    B --> C[n8n<br/>Send Reminders]
    C --> D[Telegram]
    D --> E{Resposta}
    E -->|SIM| F[n8n<br/>Medication Response]
    E -->|NÃO| F
    F --> B
    B --> A
