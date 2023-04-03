from collections.abc import Mapping


Algorithm: Mapping[int, str] = {
    1: 'SHA1',
    2: 'SHA256',
    3: 'SHA512',
    4: 'MD5',
}

DigitCount: Mapping[int, str] = {
    1: '6',
    2: '8',
}

OtpType: Mapping[int, str] = {
    1: 'hotp',
    2: 'totp',
}
