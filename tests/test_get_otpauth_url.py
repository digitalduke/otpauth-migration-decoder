from src.decoder import get_otpauth_url
from src.protobuf.otpauth_migration_pb2 import Payload


def test_get_otpauth_url():
    # arrange
    otp = Payload.OtpParameters(
        secret=b'Hello!\336\255\276\357',
        name='Example:alice@google.com',
        issuer='Example',
        type=2
    )

    # act
    result = get_otpauth_url(otp)

    # assert
    assert result == 'otpauth://totp/Example%3Aalice%40google.com?issuer=Example&secret=JBSWY3DPEHPK3PXP'
