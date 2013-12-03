=====
Simple Logger
=====
Simple Logger is a Django app that provides an easy way to you record yours
system logging messages and request exceptions.


Quick start
-----------

1. Add "simplelogger" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'simplelogger',
    )

2. Run `python manage.py syncdb` to create the simple logger models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   and you can see the log (you'll need the Admin app enabled).