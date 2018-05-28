import logging

from django.template.loader import render_to_string
from django.conf import settings

from allianceauth import hooks
from allianceauth.services.hooks import ServicesHook

from .common import NAME, ACCESS_PERM_FULL
from .tasks import DokuwikiTasks
from .urls import urlpatterns

logger = logging.getLogger(__name__)


class DokuwikiService(ServicesHook):
    def __init__(self):
        super().__init__()
        self.urlpatterns = urlpatterns
        self.name = NAME
        self.service_ctrl_template = 'services/dokuwiki/dokuwiki_service_ctrl.html'
        self.access_perm = ACCESS_PERM_FULL
        self.name_format = '{character_name}'

    def update_groups(self, user):
        logger.debug('Processing %s groups for %s' % (self.name, user))
        if self.service_active_for_user(user):
            # XXX(kormat): As any update involves regenerating the CSV file,
            # just update all groups.
            DokuwikiTasks.update_all_groups.delay()

    def update_all_groups(self):
        logger.debug('Update all %s groups called' % self.name)
        DokuwikiTasks.update_all_groups.delay()

    def service_active_for_user(self, user):
        return user.has_perm(self.access_perm)

    def render_services_ctrl(self, request):
        return render_to_string(self.service_ctrl_template, {
            'char': request.user.profile.main_character,
            'DOKUWIKI_URL': getattr(settings, 'DOKUWIKI_URL', ''),
        }, request=request)


@hooks.register('services_hook')
def register_service():
    return DokuwikiService()
