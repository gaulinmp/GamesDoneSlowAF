# GamesDoneSlowAF

Summer Game Score Tracking

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Basic Commands

### Installing / Running

If you use virtualenv, just translate `conda` ==> `virtualenv` in whatever smart way you know how, you're obviously
smarter if you're not using conda so you can figure it out.

To get up and running:

```bash
$ git clone git@github.com:gaulinmp/GamesDoneSlowAF.git
$ cd GamesDoneSlowAF
$ conda create -n gdsaf python=3.8 black
$ conda activate gdsaf
$ pip install -r requirements.txt

# yay, we have django and GamesDoneSlowAF, let's run this ship
$ cd gdsaf
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser --username=YOURUSERNAME --email=e@male.com
$ python manage.py runserver
```
Now go to http://localhost:8000 and see the magic.

To see the database backend, go to http://localhost:8000/admin/ and see
EVAN MOAR MAGIC!

### Setting Up Your Users

-   To create a **normal user account**, do it via the admin terminal. Seriously, automating the sign up is dumb so I won't do it.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser --username=YOURUSERNAME --email=e@male.com

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.
