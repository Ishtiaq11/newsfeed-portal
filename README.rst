Newsfeed Portal
===============

Personalized News Feed

Features

* User Authentication implemented
* Newsfeed based on user preferences. User can select multiple countries and sources.
* Pagination added in news index
* Scrape news in short time after news published in preference countries and sources 
* Send Email if any key preferred keywords appers in newsfeed  => In progress ...
* Newsfeed api for other app integration => In progress ...

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

Versions
--------
* Python 3.9
* Django 3.1.13
* Postgres 12.6


How to Install
--------------

.. code-block:: bash
    
    # Build the services
    docker-compose -f local.yml build
    # Run the stacks
    docker-compose -f local.yml up
    # Run in detached mode
    docker-compose up -d
    # Migrate database
    docker-compose -f local.yml run --rm django python manage.py migrate
    # Create superuser
    docker-compose -f local.yml run --rm django python manage.py createsuperuser
    # Run celery worker and beat for background news scraping
    # worker
    docker-compose -f local.yml run --rm django celery -A config.celery_app worker --loglevel=info
    # beat
    docker-compose -f local.yml run --rm django celery -A config.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    

Create Periodic Task to scrape news
------------------------------------
* Go to admin page **/admin** and login with the superuser
* Create an Interval obj of **every 10 minutes**. We don’t want the user to wait more than 15 minutes to get the updates headlines
* Create Periodic task by registering **newsfeed_portal.newsfeed.tasks.scrape_top_headlines** task and other options
    

Settings
--------

* Set newsapi API key in env file

.. code-block:: bash

  # .envs/.local/.django
  NEWS_API_KEY=<Your api key>

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy newsfeed_portal

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd newsfeed_portal
    celery -A config.celery_app worker -l info

To run celery `worker` in docker:

.. code-block:: bash

    docker-compose -f local.yml run --rm django celery -A config.celery_app worker --loglevel=info
    

To run celery `beat` in docker:

.. code-block:: bash

    docker-compose -f local.yml run --rm django celery -A config.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
