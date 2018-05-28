from django.db import models

from .common import NAME, ACCESS_PERM


class DokuwikiUser(models.Model):
    class Meta:
        # https://stackoverflow.com/a/37988538
        managed = False

        permissions = (
            (ACCESS_PERM, u"Can access the Dokuwiki service"),
        )
