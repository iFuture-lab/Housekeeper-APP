# my_project
installation:

Python (last version)
Django (last version)

install requirements
pip install -r requirements.txt

Running the project:
First migrate the database
python manage.py migrate

Start the server
gunicorn --worker-class=gevent --bind 0.0.0.0:$PORT my_project.wsgi:application or 
python manage.py runserver

 
