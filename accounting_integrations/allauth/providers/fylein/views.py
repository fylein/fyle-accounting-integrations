from fylesdk import FyleSDK
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
        # Setup the fyle API
        fyle_api = FyleSDK(
            client_id=settings.FYLE_CLIENT_ID,
            client_secret=settings.FYLE_CLIENT_SECRET,
            refresh_token=token.token_secret
        )
        profile = fyle_api.Employees.get_my_profile()
        extra_data = {
            'id': profile['data']['id'],
            'email': profile['data']['employee_email'],
            'name': profile['data']['full_name']
        }
        return self.get_provider().sociallogin_from_response(
            request, extra_data
        )


oauth2_login = OAuth2LoginView.adapter_view(FyleOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FyleOAuth2Adapter)
