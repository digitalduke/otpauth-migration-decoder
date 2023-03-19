from src.decoder import get_url_params
from src.protobuf.otpauth_migration_pb2 import Payload


def test_get_url_params():
    # arrange
    otp = Payload.OtpParameters(
        secret=b'Hello!\336\255\276\357',
        name='Example:alice@google.com',
        issuer='Example',
        type=2
    )

    # act
    result = get_url_params(otp)

    # assert
    assert result == 'issuer=Example&secret=JBSWY3DPEHPK3PXP'
