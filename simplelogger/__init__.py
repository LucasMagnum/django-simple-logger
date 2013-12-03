from django.core.signals import got_request_exception

from .models import ExceptionRecord

# connect request exception signal to a ExceptionRecord method
got_request_exception.connect(ExceptionRecord.create_from_exception)
