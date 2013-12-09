=====
Simple Logger
=====
Simple Logger is a Django app that provides an easy way to you record on database
yours system logging messages and request exceptions.


How install
------------

::

    pip install -e git+git://github.com/LucasMagnum/django-simple-logger#egg=simplelogger


Quick start
-----------

1. Add "simplelogger" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'simplelogger',
    )

2. Add the "simplelogger_dbhandler" to your LOGGING setting like this::

    LOGGING = {
        ...

        'handlers': {
            ...
            'simplelogger_dbhandler': {
                'class': 'simplelogger.handlers.DBLogRecordHandler'
            },
        },

    }

3. Now, you can use "simplelogger_dbhandler", if you want log all messages, do that::

    LOGGING = {

     'loggers': {
            ...

            '': {
                'handlers': ['simplelogger_dbhandler'],
                'level': DEBUG,
                'propagate': True,
            }
        }
    }

4. Run `python manage.py syncdb` to create the simple logger models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   and you can see the log (you'll need the Admin app enabled).


Reference
---------

Django logging documentation: https://docs.djangoproject.com/en/1.5/topics/logging/

Python logging documentation: http://docs.python.org/2.7/library/logging.html#module-logging

Issues
---------
https://github.com/LucasMagnum/django-simple-logger/issues
