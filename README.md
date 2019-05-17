# fyle-accounting-integrations
Integrating Fyle with Accounting Systems

## Dev Environment Setup

Follow these steps to setup your dev environment

* Install requirements using `pip install -r requirements.txt`
* Run migrations using `python manage.py migrate`
* Create a superuser using `python manage.py createsuperuser`
* Copy the environments file `cp .env.sample .env` and update the variables
* Start the server using `python manage.py runserver`

Setup the Oauth2 Integration 

* Open the admin panel at http://127.0.0.1:8000/admin
* Edit the existing `Sites` object and set the domain name to `127.0.0.1`
* Add a `social application` with provider as Fyle and other relevant details.

That's it now you have enabled Fyle Oauth2 integration for login.

Load the seed data with the command `python manage.py loaddata seed_data`
