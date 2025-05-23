import pytest
from app.models import User
from tests.utils.random_user import create_random_user
from lxml import etree

@pytest.fixture
def persisted_user() -> User:
    return create_random_user()


def test_(
    client,
    persisted_user: User,
):
    response = client.get('/')

    assert response.status_code == 200

    tree = etree.HTML(response.data)
    factual_table_row = tree.xpath("//table/tbody/tr[1]/td/text()")
    expected_table_row = [
        persisted_user.gender,
        persisted_user.name.first,
        persisted_user.name.last,
        persisted_user.phone,
        persisted_user.email,
        f"{persisted_user.location.country}, {persisted_user.location.city}",
    ]
    fields_count = len(expected_table_row)

    assert factual_table_row[:fields_count] == expected_table_row
