from unittest import mock

from idealista import Idealista


@mock.patch("idealista.api.get_token")
def test_authenticate_sets_returned_token(mock_get_token):
    client_id = "aaabbbcc"
    expected_token = {"token": "abcxyz"}
    mock_get_token.return_value = expected_token

    api = Idealista.authenticate(client_id=client_id, client_secret=...)

    assert api.client_id == client_id
    assert api.token == expected_token
