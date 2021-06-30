import pytest
from click import BadParameter

from src.decoder import validate_migration


def test_validate_migration__migration__ok():
    # arrange
    migration = 'otpauth-migration://offline?data=CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC'

    # act
    result = validate_migration(None, None, migration)

    # assert
    assert result == ['CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC']


@pytest.mark.parametrize(
    'broken_migration',
    [
        'otpauth-migration://online?data=CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
        'CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
        'offline?data=CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
        'otpauth-migration://online?data=Cu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
        'data=CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC',
    ]
)
def test_validate_migration__broken_migration__raise(broken_migration):
    # act & assert
    with pytest.raises(BadParameter):
        validate_migration(None, None, broken_migration)
