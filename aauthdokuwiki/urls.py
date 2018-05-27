from django.conf.urls import url

from . import views

urlpatterns = [
    # Dokuwiki SSO
    url(r'^dokuwiki/sso$', views.dokuwiki_sso, name='auth_dokuwiki_sso'),
]
