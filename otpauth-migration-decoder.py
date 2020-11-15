import argparse
import sys
from base64 import b64decode, b32encode
from typing import Dict, Any, List
from urllib.parse import urlparse, parse_qs, ParseResult, urlencode

from otpauth_enums import Algorithm, DigitCount, OtpType
from otpauth_migration_pb2 import Payload

SCHEME = 'otpauth-migration'
HOSTNAME = 'offline'


parser = argparse.ArgumentParser(
    description="Convert otpauth-migration to plain link",
)
parser.add_argument(
    'migration',
    help='otpauth-migration link text',
    action='store',
    type=str,
)


def is_migration_incorrect(
        *,
        parsed_url: ParseResult,
        parsed_qs: Dict[str, Any],
) -> bool:
    return (
            parsed_url.scheme != SCHEME or
            parsed_url.hostname != HOSTNAME or
            'data' not in parsed_qs or
            not isinstance(parsed_qs['data'], list)
    )


def decoded_data(data: List[str]) -> bytes:
    for data_item in data:
        yield b64decode(data_item)


def terminate(
        *,
        error: str,
        code: int = 1,
) -> None:
    print(error, file=sys.stderr)
    exit(code=code)


def decode_secret(secret: bytes) -> str:
    return str(b32encode(secret), 'utf-8').replace('=', '')


def get_url_params(otp) -> str:
    params = dict()

    if otp.algorithm:
        params.update({'algorithm': Algorithm.get(otp.algorithm, '')})
    if otp.digits:
        params.update({'digits': DigitCount.get(otp.digits, '')})
    if otp.issuer:
        params.update({'issuer': otp.issuer})
    if otp.secret:
        otp_secret = decode_secret(otp.secret)
        params.update({'secret': otp_secret})

    return urlencode(params)


def get_otpauth_url(otp) -> str:
    otp_type = OtpType.get(otp.type, '')
    otp_name = otp.name
    otp_params = get_url_params(otp)

    return f'otpauth://{otp_type}/{otp_name}?{otp_params}'


if __name__ == '__main__':
    args = parser.parse_args()

    url: ParseResult = urlparse(args.migration)
    qs: Dict[str, Any] = parse_qs(url.query)

    if is_migration_incorrect(parsed_url=url, parsed_qs=qs):
        terminate(error='Ensure your otpauth-migration string are correct')

    for payload in decoded_data(data=qs['data']):
        migration_payload = Payload()
        migration_payload.ParseFromString(payload)

        for otp_item in migration_payload.otp_parameters:
            print(get_otpauth_url(otp_item), file=sys.stdout)
