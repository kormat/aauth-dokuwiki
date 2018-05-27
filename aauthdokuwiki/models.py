from django.contrib.auth.models import User
from django.db import models

from .common import NAME, ACCESS_PERM


class DokuwikiUser(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                related_name=NAME)
    enabled = models.BooleanField()

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = (
            (ACCESS_PERM, u"Can access the Dokuwiki service"),
        )
