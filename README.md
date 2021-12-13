# fabrika
Тестовое для ФР, приложение для голосования.

Cтек:
django + postgresql + django-rest-framework + swagger

Инструкция по разворачиванию приложения локально:
```
1. клонировать репозиторий
git clone https://github.com/Zlofey/fabrika

2. создать виртуальное окружение
cd fabrika
virtualenv venv
source venv/bin/activate

3. установить зависимости
python -m pip install -U pip setuptools
pip install -U -r requirements.txt

4. поменять имя файла .env.template на .env и заполнить в соответсвии с вашей бд

5. применить миграции
python manage.py migrate

6. создать суперюзера
python manage.py createsuperuser

7. запустить сервер
python manage.py runserver
```
Можно протестировать онлайн:
[heroku](https://fb-poll-app.herokuapp.com/swagger/) (логопас админки admin 123)

Создание опросов реализовано через админку( /admin )

Остальной функционал описан в swagger( /swagger ) 
