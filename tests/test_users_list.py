import pytest
from app.models import User
from tests.utils.random_user import create_random_user_in_bulk
from tests.utils.assertations import (
    asssert_pages_count,
    assert_rows_count,
)
from lxml import etree
import typing
import re


def test_user_view(client, persisted_user: User):
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


@pytest.mark.parametrize(
    'users_amount, pages_expected, users_per_page',
    (
        (10, 1, (10,)),
        (12, 2, (10, 2)),
        (35, 4, (10, 10, 10, 5)),
    )
)
def test_pagination(
    client,
    users_amount: int,
    pages_expected: int,
    users_per_page: typing.Iterable[int],
):
    ROWS_PER_PAGE = 10

    create_random_user_in_bulk(users_amount)

    response = client.get('/')
    assert response.status_code == 200

    tree = etree.HTML(response.data)
    assert_rows_count(tree, users_per_page[0])
    asssert_pages_count(tree, pages_expected)

    for users_expected in users_per_page[1:]:
        next_page_url = str(tree.xpath("//div[@id='pagination']/a[text()='Next']/@href")[0])

        response = client.get(next_page_url)
        assert response.status_code == 200

        tree = etree.HTML(response.data)
        assert_rows_count(tree, users_expected)
