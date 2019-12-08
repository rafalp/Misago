from ..token import decode_token, encode_token


SECRET = "secret"


def test_token_can_be_encoded_and_decoded_back():
    payload = {"test": "ok!"}
    token = encode_token(SECRET, payload)
    assert decode_token(SECRET, token) == payload
