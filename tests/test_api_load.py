import pytest
from tests.utils.assertations import assert_total_users
from unittest.mock import Mock, patch
from tests.utils.user_json import user_json
from lxml import etree


@pytest.fixture()
def mock_fetch_users():
    with patch('app.utils.load_service.fetch_users_from_api') as mock:
        def side_effect(amount: int):
            return [user_json for _ in range(amount)]
        mock.side_effect = side_effect
        yield mock



@pytest.mark.parametrize(
    'users_amount',
    (5, 10, 15)
)
def test_api_load(client, mock_fetch_users, users_amount: int):
    payload = {
        "users_amount": users_amount,
    }
    response = client.post('/', data=payload)

    assert response.status_code == 200

    mock_fetch_users.assert_called_once_with(amount=users_amount)

    tree = etree.HTML(response.data)
    assert_total_users(tree, users_amount)
