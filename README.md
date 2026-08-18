# Ticket Support Bot

**PoC автоматизации обработки тикетов поддержки.**

---

## Сценарии

1. **Happy Path**  
   Вопрос: *"Как восстановить пароль?"*  
   → Автоответ из базы знаний.

2. **Fallback Path**  
   Вопрос: *"Как оплатить зарубежный сервис?"*  
   → Эскалация оператору.

---

## Запуск

```bash
pip install -r requirements.txt
python indexer.py
python bot.py

## Пример

Пользователь пишет 2 вопроса: простой (happy path) и сложный, требующий эскалации.
<img width="1080" height="2392" alt="image" src="https://github.com/user-attachments/assets/6e7e8d2e-45d2-4f5c-b834-4a906f3c5302" />

На сложный отвечает поддержка.
<img width="1257" height="155" alt="image" src="https://github.com/user-attachments/assets/87611d89-c48d-4cad-858b-482846baa70f" />

Все события записываются в лог.
<img width="1272" height="136" alt="image" src="https://github.com/user-attachments/assets/8a5cc64c-4d06-40eb-bb61-8aba2effa126" />
