from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

UserModel = getattr(settings, 'AUTH_USER_MODEL', User)


class LogRecord(models.Model):
    """
        A simple log record, will be created always that logging module is
        called.

        `name` is a name of used logger
        `level` is level of message (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        `msg` is a logging message
        `extra` is a json with attributes of LogRecord.
    """
    LEVEL_CHOICES = (
        (0, 'NOTSET'),
        (10, 'DEBUG'),
        (20, 'INFO'),
        (30, 'WARNING'),
        (40, 'ERROR'),
        (50, 'CRITICAL')
    )

    name = models.CharField(_('name'), max_length=120)
    level = models.PositiveIntegerField(default=0, choices=LEVEL_CHOICES)

    msg = models.TextField()
    extra = models.TextField(blank=True)

    added_on = models.DateTimeField(_('added on'), auto_now_add=True)
    added_by = models.ForeignKey(
        UserModel, verbose_name=_('added by'), blank=True, null=True)

    class Meta:
        verbose_name = _('Log Record')
        verbose_name_plural = _('Log Records')
        ordering = ['-added_on']

    def __unicode__(self):
        return u'%s-%s' % (self.get_level_display(), self.msg)

    @classmethod
    def add(cls, **kwargs):
        cls.objects.create(**kwargs)

    @classmethod
    def count(cls):
        return cls.objects.count()


class ExceptionRecord(models.Model):
    """
        A simple Exception record, will be create whenever that
        django encounters a exception while processing an
        incoming HTTP request or manually when you call a
        `create_from_exception` method in a exception context.
    """
    type = models.CharField(_('type'), blank=True, max_length=128, db_index=True)
    value = models.TextField(_('value'))

    traceback = models.TextField(blank=True)
    traceback_html = models.TextField(blank=True)

    path = models.URLField(_('path'), null=True, blank=True, verify_exists=False)
    error_id = models.CharField(max_length=20, blank=True)

    added_on = models.DateTimeField(_('added on'), auto_now_add=True)
    added_by = models.ForeignKey(
        UserModel, verbose_name=_('added by'), blank=True, null=True)

    class Meta:
        verbose_name = _('Exception')
        verbose_name_plural = _('Exceptions')
        ordering = ['-added_by']

    def __unicode__(self):
        return "%s: %s" % (self.type, self.value)

    @classmethod
    def count(cls):
        return cls.objects.count()

    @staticmethod
    def create_from_exception(sender, request=None, *args, **kwargs):
        """
            Create a ExceptionRecord from django got_request_exception signal.
            `sender` isn't used
            `request` the incoming request
            `exc_info` the exception values
        """
        import hashlib
        import sys
        import traceback

        from django.http import Http404
        from django.views.debug import ExceptionReporter

        exc_info = kwargs.get('exc_info')
        if exc_info is None:
            exc_info = sys.exc_info()

        typ, value, trace = exc_info

        if not issubclass(typ, Http404):
            traceback_html = ExceptionReporter(
                request, typ, value, trace).get_traceback_html()

            traceback_fmt = '\n'.join(traceback.format_exception(
                typ, value, trace))

            error = ExceptionRecord.objects.create(
                type=typ.__name__,
                traceback_html=traceback_html,
                value=value,
                added_by=getattr(request, 'user', None),
                traceback=traceback_fmt,
            )

            error_id = hashlib.md5(str(error.id)).hexdigest()[:10]
            error.error_id = error_id

            if request:
                error.path = request.build_absolute_uri()
                request.error_id = error_id

            error.save()
