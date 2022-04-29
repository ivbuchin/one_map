# One Map 
**«One Map»** — проект образовательной платформы, содержащей онлайн-учебник, форум и элементы социальной сети. Проект написан на Django.

Чтобы запустить проект, выполните следующие действия:
1. Скачайте код проекта
2. Создайте и активируйте виртуальное окружение
4. Установите зависимости:

        pip install -r requirements/dev.txt

5. Сгенерируйте SECRET KEY (например, на сайте https://djecrety.ir/) и вставьте его в настройки проекта
6. Создайте и выполните миграции: 

        python manage.py makemigrations
        python manage.py migrate

10. Создайте суперпользователя: 

        python manage.py createsuperuser

12. Запустите локальный сервер:

        python manage.py runserver

14. Откроейте сайт проекта, введя в адресной строке браузера: [127.0.0.1:8000](http://127.0.0.1:8000/)
15. Для доступа к админ-панели, введите в адресной строке: [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin/)

<br>

<img width="800px" alt="printscreen" src="https://github.com/ivbuchin/one_map/blob/master/printscreen.png">
