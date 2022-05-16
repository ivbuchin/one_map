# One Map 
**«One Map»** is a project of an educational platform containing an online textbook, a forum and elements of a social network. The project is written in Django.

To start the project, follow these steps:
1. Download the project code
2. Create and activate a virtual environment
4. Install dependencies:

        pip install -r requirements/dev.txt

5. Generate a SECRET KEY (for example, on the website https://djecrety.ir /) and paste it into the project settings
6. Create and perform migrations: 

        python manage.py makemigrations
        python manage.py migrate

10. Create a Superuser:

        python manage.py createsuperuser

12. Start the local server:

        python manage.py runserver

14. Open the project website by typing in the browser address bar: 127.0.0.1:8000
15. To access the admin panel, enter in the address bar: 127.0.0.1:8000/admin

<br>

<img width="800px" alt="printscreen" src="https://github.com/ivbuchin/one_map/blob/master/printscreen.png">
