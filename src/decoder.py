from base64 import (
    b32encode,
    b64decode,
)
from collections.abc import Generator
from typing import (
    Any,
    Dict,
    List,
    Union,
)
from urllib.parse import (
    ParseResult,
    parse_qs,
    quote,
    urlencode,
    urlparse,
)

import click
from PIL import Image
from pyzbar.pyzbar import decode as pyzbar_decode
from pyzbar.pyzbar_error import PyZbarError

from enums import (
    Algorithm,
    DigitCount,
    OtpType,
)
from protobuf.otpauth_migration_pb2 import Payload


SCHEME = 'otpauth-migration'
HOSTNAME = 'offline'
PAYLOAD_MARK = 'data'
EXAMPLE_PAYLOAD = 'CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC'
EXAMPLE_MIGRATION = f'{SCHEME}://{HOSTNAME}?{PAYLOAD_MARK}={EXAMPLE_PAYLOAD}'


def is_migration_incorrect(
        *,
        parsed_url: ParseResult,
        parsed_qs: Dict[str, Any],
) -> bool:
    return (
            parsed_url.scheme != SCHEME
            or parsed_url.hostname != HOSTNAME
            or PAYLOAD_MARK not in parsed_qs
            or not isinstance(parsed_qs[PAYLOAD_MARK], list)
    )


def decoded_data(data: List[str]) -> Generator:
    for data_item in data:
        yield b64decode(data_item)


def decode_secret(secret: bytes) -> str:
    return str(b32encode(secret), 'utf-8').replace('=', '')


def get_url_params(otp: Payload.OtpParameters) -> str:
    params: dict[str, Union[str, int]] = {}

    if otp.algorithm:
        params.update(algorithm=Algorithm.get(otp.algorithm, ''))
    if otp.digits:
        params.update(digits=DigitCount.get(otp.digits, ''))
    if otp.issuer:
        params.update(issuer=otp.issuer)
    if otp.secret:
        otp_secret = decode_secret(otp.secret)
        params.update(secret=otp_secret)

    return urlencode(params)


def get_otpauth_url(otp: Payload.OtpParameters) -> str:
    otp_type = OtpType.get(otp.type, '')
    otp_name = quote(otp.name)
    otp_params = get_url_params(otp)

    return f'otpauth://{otp_type}/{otp_name}?{otp_params}'


def validate_migration(ctx: click.Context, param: click.Option, migration: str) -> list[str]:
    url: ParseResult = urlparse(migration)
    qs: Dict[str, Any] = parse_qs(url.query)

    if is_migration_incorrect(parsed_url=url, parsed_qs=qs):
        raise click.BadParameter(f'migration must be like "{EXAMPLE_MIGRATION}"')

    return qs[PAYLOAD_MARK]


@click.group()
def cli():
    """otpauth-migration decoder"""


@cli.command()
@click.option(
    '--migration',
    'migration_data',
    type=click.UNPROCESSED,
    callback=validate_migration,
    help='otpauth-migration link text',
)
def decode(migration_data: list[str]):
    """Convert Google Authenticator data to plain otpauth links"""

    for payload in decoded_data(data=migration_data):
        migration_payload = Payload()
        migration_payload.ParseFromString(payload)

        for otp_item in migration_payload.otp_parameters:
            print(get_otpauth_url(otp_item))


@cli.command()
@click.option(
    '--file',
    'filename',
    type=click.Path(exists=True),
    help='file name or path with file name'
)
def extract(filename: str):
    """Extract otpauth-migration from qr-code image"""
    with Image.open(filename) as qr_code_image:
        try:
            data = pyzbar_decode(qr_code_image)
        except PyZbarError:
            click.echo('Unsupported image format')

        for item in data:
            click.echo(item.data)


if __name__ == '__main__':
    cli()
