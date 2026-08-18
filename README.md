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


## Демонстрация


**Пользователь пишет 2 вопроса: простой (happy path) и сложный, требующий эскалации.**

<img width="1080" height="2392" alt="user_q" src="https://github.com/user-attachments/assets/1894ce8d-9b61-4061-9927-406a8ab1f128" />

**На сложный отвечает поддержка.**

<img width="1222" height="168" alt="support_a" src="https://github.com/user-attachments/assets/b5e1b6df-43f0-4b1e-a24d-824a513d5ecb" />

**Все события записываются в лог.**

<img width="1272" height="136" alt="logs" src="https://github.com/user-attachments/assets/81eb49ce-a5ce-42ec-a871-36db66446939" />
