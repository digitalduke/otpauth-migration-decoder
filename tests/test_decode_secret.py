import pytest

from src.decoder import decode_secret


@pytest.mark.parametrize(
    'secret,expected_result',
    [
        (b'Hello!\xde\xad\xbe\xef', 'JBSWY3DPEHPK3PXP', ),
        (b'Hello!', 'JBSWY3DPEE',),
        (b'\xde\xad\xbe\xef', '32W353Y',),
    ],
)
def test_decode_secret(secret, expected_result):
    # act
    result = decode_secret(secret)

    # assert
    assert result == expected_result
