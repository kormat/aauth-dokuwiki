import logging
import csv

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task

from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter
from allianceauth.services.tasks import QueueOnce

from .common import (
    ACCESS_PERM_FULL,
    get_sanitized_username,
    output_path,
    user_groups,
)
from .models import DokuwikiUser

logger = logging.getLogger(__name__)


class DokuwikiTasks:
    def __init__(self):
        pass

    @staticmethod
    @shared_task(name='dokuwiki.update_all_groups')
    def update_all_groups():
        logger.debug("Updating ALL dokuwiki groups")
        d = {}
        for user in User.objects.all():
            if not user.has_perm(ACCESS_PERM_FULL):
                continue
            name = get_sanitized_username(user)
            if name is None:
                logger.debug("User %s has no main char, skipping", user)
                continue
            groups = user_groups(user)
            logger.debug("Export: user %s (%s) groups: %s", user, name, groups)
            d[name] = groups
        path = output_path()
        with open(path, "w", newline="") as f:
            w = csv.writer(f, lineterminator='\n')
            for name in sorted(d):
                w.writerow([name] + d[name])
        logger.info("Export written to %s", path)
