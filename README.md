# fabrika
test app for FR

django + postgresql + django-rest-framework + swagger

инструкция по разворачиванию приложения локально:
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

Создание опросов реализовано через админку /admin

Остальной функционал описан в swagger /swagger 
