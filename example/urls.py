import re

from django.conf import settings
from django.conf.urls import include, patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forms/', include('forms_builder.forms.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'serve', kwargs={
            'document_root': settings.STATIC_ROOT,
        }),
    )

    urlpatterns += patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), 'serve', kwargs={
            'document_root': settings.MEDIA_ROOT,
        }),
    )

urlpatterns += patterns('',
    url(r'', include('fluent_pages.urls')),
)
