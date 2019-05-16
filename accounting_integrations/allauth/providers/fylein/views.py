import requests

from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from accounting_integrations.allauth.providers.fylein.provider import FyleProvider


class FyleOAuth2Adapter(OAuth2Adapter):
    provider_id = FyleProvider.id

    base_url = settings.FYLE_BASE_URL.rstrip('/')

    access_token_url = '{0}/api/oauth/token'.format(base_url)
    authorize_url = '{0}/app/main/#/oauth/authorize'.format(base_url)
    profile_url = '{0}/user'.format(base_url)

    def complete_login(self, request, app, token, **kwargs):
        # params = {'access_token': token.token}
        # resp = requests.get(self.profile_url, params=params)
        extra_data = {
            'id': 1234,
            'email': 'admin@fyledev.in',
            'name': 'Abhishek Ram'
        }
        return self.get_provider().sociallogin_from_response(
            request, extra_data
        )


oauth2_login = OAuth2LoginView.adapter_view(FyleOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FyleOAuth2Adapter)
