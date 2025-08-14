from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to include extra user info in JWT token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token
def get_authenticated_user(request):
    """
    Extract and return the authenticated user from the request using JWT authentication.

    Raises AuthenticationFailed if the token is invalid or user not authenticated.
    """
    jwt_authenticator = JWTAuthentication()

    # This will validate the token and return (user, validated_token)
    user_auth_tuple = jwt_authenticator.authenticate(request)

    if user_auth_tuple is None:
        raise AuthenticationFailed('Authentication credentials were not provided or invalid.')

    user, validated_token = user_auth_tuple
    return user
