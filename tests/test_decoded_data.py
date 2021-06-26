from src.decoder import decoded_data


def test_decoded_data__expected():
    # arrange
    data = ['CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC', ]

    # act
    generator = decoded_data(data)
    result = list(generator)

    # assert
    assert result == [b'\n1\n\nHello!\xde\xad\xbe\xef\x12\x18Example:alice@google.com\x1a\x07Example0\x02', ]


def test_decoded_data__list__expected():
    # arrange
    data = [
        'CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
        'CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
    ]

    # act
    generator = decoded_data(data)
    result = list(generator)

    # assert
    assert result == [
        b'\n1\n\nHello!\xde\xad\xbe\xef\x12\x18Example:alice@google.com\x1a\x07Example0\x02',
        b'\n1\n\nHello!\xde\xad\xbe\xef\x12\x18Example:alice@google.com\x1a\x07Example0\x02',
    ]
