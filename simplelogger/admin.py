from django.contrib import admin

from .models import LogRecord, ExceptionRecord


class CommonAttrMixin(object):
    raw_id_fields = ('added_by',)
    readonly_fields = ('added_on',)
    date_hierarchy = 'added_on'
    ordering = ('-added_by',)


class LogRecordAdmin(CommonAttrMixin, admin.ModelAdmin):
    list_select_related = True

    list_display = ('level_name', 'name', 'msg', 'extra', 'added_by')
    list_filter = ('level', 'name')

    search_fields = ('name', 'msg')

    def level_name(self, obj):
        return obj.get_level_display()
    level_name.short_description = 'level'
    level_name.admin_order_field = 'level'


class ExceptionRecordAdmin(CommonAttrMixin, admin.ModelAdmin):
    list_select_related = True

    list_display = ('type', 'value', 'path', 'error_id')
    list_filter = ('type',)

    search_fields = ('type', 'value', 'path', 'error_id')
    readonly_fields = ('added_on', 'error_id', 'path', 'added_by')


admin.site.register(LogRecord, LogRecordAdmin)
admin.site.register(ExceptionRecord, ExceptionRecordAdmin)
