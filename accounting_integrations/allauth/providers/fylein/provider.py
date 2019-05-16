from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FyleAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('html_url')

    def get_avatar_url(self):
        return self.account.extra_data.get('avatar_url')

    def to_str(self):
        dflt = super().to_str()
        return next(
            value
            for value in (
                self.account.extra_data.get('name', None),
                self.account.extra_data.get('login', None),
                dflt
            )
            if value is not None
        )


class FyleProvider(OAuth2Provider):
    id = 'fyle'
    name = 'Fyle'
    account_class = FyleAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    name=data.get('name'))


provider_classes = [FyleProvider]
