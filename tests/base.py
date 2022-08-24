from managers.auth import AuthManager


def generate_token(user):
    """
    Create a token.

    :param user: UserModel object
    :return: token: string, a valid token
    """
    return AuthManager.encode_token(user)


def mock_uuid():
    return "11111111-1111-1111-1111-111111111111"
