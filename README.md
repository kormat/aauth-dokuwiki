This is a [DokuWiki](https://www.dokuwiki.org/) integration for
[Alliance Auth](https://github.com/allianceauth/allianceauth). This module
implements SSO and group export from aauth. See
[here](https://github.com/pcd1193182/dokuwiki-discourse-sso) for the
corresponding auth plugin for dokuwiki.

This module is *heavily* based on the discourse integration that is already in
allianceauth.

To install:
  Run `pip install .` in the top directory.

Add the following entries to `settings/local.py`:
```
DOKUWIKI_URL = 'https://doku.example.com'
## Set this to a long random string.
DOKUWIKI_SSO_SECRET = ''
## Default location/name:
DOKUWIKI_GROUP_PATH = '/tmp/dokuwiki_groups.csv'
## Uncomment to see debug logging:
#LOGGING['loggers']['aauthdokuwiki'] = {
#    'handlers': ['log_file', 'console', 'notifications'],
#    'level': 'DEBUG',
#    'propagate': False,
#}
```
