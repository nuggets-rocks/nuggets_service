from rest_framework.authentication import TokenAuthentication
from nuggets_api.models import NuggetsToken

class MyOwnTokenAuthentication(TokenAuthentication):
    model = NuggetsToken