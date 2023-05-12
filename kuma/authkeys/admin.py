from django.contrib import admin

from kuma.core.urlresolvers import reverse

from .models import Key, KeyAction


def history_link(self):
    url = f"{reverse('admin:authkeys_keyaction_changelist')}?key__exact={self.id}"
    count = self.history.count()
    what = 'action' if count == 1 else 'actions'
    return f'<a href="{url}">{count}&nbsp;{what}</a>'

history_link.allow_tags = True
history_link.short_description = 'Usage history'


class KeyAdmin(admin.ModelAdmin):
    fields = ('description',)
    list_display = ('id', 'user', 'created', history_link, 'key',
                    'description')
    ordering = ('-created', 'user')
    search_fields = ('key', 'description', 'user__username')


def key_link(self):
    key = self.key
    url = reverse('admin:authkeys_key_change',
                  args=[key.id])
    return f'<a href="{url}">{key.user} (#{key.id})</a>'

key_link.allow_tags = True
key_link.short_description = 'Key'


def content_object_link(self):
    obj = self.content_object
    url_key = f'admin:{obj._meta.app_label}_{obj._meta.module_name}_change'
    url = reverse(url_key, args=[obj.id])
    return f'<a href="{url}">{self.content_type} (#{obj.pk})</a>'

content_object_link.allow_tags = True
content_object_link.short_description = 'Object'


class KeyActionAdmin(admin.ModelAdmin):
    fields = ('notes',)
    list_display = ('id', 'created', key_link, 'action',
                    content_object_link, 'notes')
    list_filter = ('action', 'content_type')
    ordering = ('-id',)
    search_fields = ('action', 'key__key', 'key__user__username', 'notes')


admin.site.register(Key, KeyAdmin)
admin.site.register(KeyAction, KeyActionAdmin)
