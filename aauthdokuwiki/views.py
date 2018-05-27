from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .common import ACCESS_PERM_FULL, get_sanitized_username
from .tasks import DokuwikiTasks
from .models import DokuwikiUser

import base64
import hmac
import hashlib

try:
    from urllib import unquote, urlencode
except ImportError: #py3
    from urllib.parse import unquote, urlencode
try:
    from urlparse import parse_qs
except ImportError: #py3
    from urllib.parse import parse_qs

import logging

logger = logging.getLogger(__name__)




@login_required
def dokuwiki_sso(request):

    # Check if user has access
    if not request.user.has_perm(ACCESS_PERM_FULL):
        messages.error(request, 'You are not authorized to access Dokuwiki.')
        logger.warning('User %s attempted to access Dokuwiki but does not have permission.' % request.user)
        return redirect('authentication:dashboard')

    if not request.user.profile.main_character:
        messages.error(request, "You must have a main character set to access Dokuwiki.")
        logger.warning('User %s attempted to access Dokuwiki but does not have a main character.' % request.user)
        return redirect('authentication:characters')

    main_char = request.user.profile.main_character

    payload = request.GET.get('sso')
    signature = request.GET.get('sig')

    if None in [payload, signature]:
        messages.error(request, 'No SSO payload or signature. Please contact support if this problem persists.')
        return redirect('authentication:dashboard')

    # Validate the payload
    try:
        payload = unquote(payload).encode('utf-8')
        decoded = base64.decodestring(payload).decode('utf-8')
        assert 'nonce' in decoded
        assert len(payload) > 0
    except AssertionError:
        messages.error(request, 'Invalid payload. Please contact support if this problem persists.')
        return redirect('authentication:dashboard')

    key = str(settings.DOKUWIKI_SSO_SECRET).encode('utf-8')
    h = hmac.new(key, payload, digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        messages.error(request, 'Invalid payload. Please contact support if this problem persists.')
        return redirect('authentication:dashboard')

    ## Build the return payload

    username = get_sanitized_username(request.user)

    qs = parse_qs(decoded)
    params = {
        'nonce': qs['nonce'][0],
        'email': request.user.email,
        'external_id': request.user.pk,
        'username': username,
        'name': username,
    }

    if main_char:
        params['avatar_url'] = 'https://image.eveonline.com/Character/%s_256.jpg' % main_char.character_id

    return_payload = base64.encodestring(urlencode(params).encode('utf-8'))
    h = hmac.new(key, return_payload, digestmod=hashlib.sha256)
    query_string = urlencode({'sso': return_payload, 'sig': h.hexdigest()})

    # Record activation and queue group sync
    if not DokuwikiTasks.has_account(request.user):
        dokuwiki_user = DiscourseUser()
        dokuwiki_user.user = request.user
        dokuwiki_user.enabled = True
        dokuwiki_user.save()
        DokuwikiTasks.update_groups.delay()

    # Redirect back to Dokuwiki
    url = '%s/session/sso_login' % settings.DOKUWIKI_URL
    return redirect('%s?%s' % (url, query_string))

