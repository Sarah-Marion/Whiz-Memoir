from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import views as core_views


# Routing paths

urlpatterns = [
    # web pages
    url(r'^all/$', views.view_all_entries, name="view_all"),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^future/$', views.view_all_entries, {"future_only": "True"},name="view_future"),
    url(r'^chronicles/$', views.view_chronicles, name="view_chronicles"),
    url(r'^next-seven/$', views.view_next_seven_days_entries, name="home"),
    url(r'^view_month/(?P<year>\d+)/(?P<month>\d+)/$', views.view_month_entries, name="view_month"),
    # url(r'^/$', views.view_month_entries, name="view_month"),
    # Ajax urls
    url(r'^toggle-todo/(?P<todo_id>\d+)/$', views.toggle_todo, name="toggle_todo"),
    # Form urls
    url(r'^create/$', views.create_entry, name="create_entry"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
