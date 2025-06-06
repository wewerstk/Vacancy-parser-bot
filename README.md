# Vacancy-parser-bot

## Installation
Необходимо добавить бота в группу, куда он будет отсылать вакансии и сделать его администратором. Затем запустить его и в нужном топике выполнить команду **\chat_id**. В результате команды, будет получен chat_id и thread_id, которые необходимо добавить в файле handlers.py в функцию send_and_dispatch() в соответствующие параметры chat_id и message_thread_id.

![image](https://github.com/user-attachments/assets/f03cd50a-647d-4efd-8635-000c49dc6e37)

### Файл run.py
Для того, чтобы настроитт расписание, необходимо открыть файл run.py и установить желаемое время (hour и minute) для ежедневной отправки сообщения в группу.

![image](https://github.com/user-attachments/assets/85f3c61a-1758-4fd1-b190-1f0c9c74d2dd)

## Загрузка на сервер
На сервере необходимо создать папку для проекта, перейти в неё и настроить виртуальное окружение:

```bash 
mkdir -p bots/vacancyparser
cd bots/vacancyparser
screen -S vacancyparser
python -m venv .venv
source .venv/bin/activate
pip install -r requirments.txt
```

## Запуск бота 
python run.py

## Работа с сессией терминала бота
### Выход из сессии без остановки
```bash 
ctrl+A + ctrl+D
```

### Возвращение в сессию
```bash 
screen -r vacancyparser
```

### Выключение бота
В сессии терминала бота
```bash 
ctrl+C
```
