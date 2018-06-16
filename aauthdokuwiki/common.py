from django.conf import settings

from allianceauth.services.hooks import NameFormatter

NAME = "aauthdokuwiki"
ACCESS_PERM = "access_dokuwiki"
ACCESS_PERM_FULL = "%s.%s" % (NAME, ACCESS_PERM)

def get_username(user):
    from .auth_hooks import DokuwikiService
    return NameFormatter(DokuwikiService(), user).format_name()

def _sanitize(name):
    return "".join([c for c in name if c.isalnum()])

def get_sanitized_username(user):
    return _sanitize(get_username(user))

def output_path():
    return getattr(settings, "DOKUWIKI_GROUP_PATH", '/tmp/dokuwiki_groups.csv')

def user_groups(user):
    groups = [_sanitize(user.profile.state.name)]
    for g in user.groups.all():
        groups.append(_sanitize(g.name))
    return groups
