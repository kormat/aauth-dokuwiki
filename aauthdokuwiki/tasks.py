import logging
import csv

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task

from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter
from allianceauth.services.tasks import QueueOnce

from .common import get_sanitized_username, user_groups, output_path
from .models import DokuwikiUser

logger = logging.getLogger(__name__)


class DokuwikiTasks:
    def __init__(self):
        pass

    @classmethod
    def delete_user(cls, user, notify_user=False):
        if cls.has_account(user):
            logger.debug("User %s has a Dokuwiki account. Disabling login." % user)
            user.dokuwiki.delete()
            if notify_user:
                notify(user, 'Dokuwiki Account Disabled', level='danger')
            return True
        return False

    @staticmethod
    def has_account(user):
        """
        Check if the user has a dokuwiki account
        :param user: django.contrib.auth.models.User
        :return: bool
        """
        try:
            return user.dokuwiki.enabled
        except ObjectDoesNotExist:
            return False

    @staticmethod
    @shared_task(name='dokuwiki.update_all_groups')
    def update_all_groups():
        logger.debug("Updating ALL dokuwiki groups")
        d = {}
        for doku_user in DokuwikiUser.objects.filter(enabled=True):
            user = User.objects.get(pk=doku_user.user.pk)
            name = get_sanitized_username(user)
            if name is None:
                logger.debug("User %s has no main char, skipping", user)
                continue
            groups = user_groups(user)
            logger.debug("Export: user %s (%s) groups: %s", user, name, groups)
            d[name] = groups
        path = output_path()
        with open(path, "w") as f:
            w = csv.writer(f)
            for name in sorted(d):
                w.writerow([name] + d[name])
        logger.info("Export written to %s", path)
