import typing
import re


def assert_field_by_data_id(tree, data_id: str, expected_text: typing.Any):
    el = tree.xpath(f"//*[@data-field-id='{data_id}']/text()")
    assert len(el) > 0, f"Field with id {data_id} not found"
    assert el[0] == str(expected_text), f"failed on data-field-id={data_id}"


def asssert_pages_count(tree, expected_pages: int) -> None:
    pagination_span = tree.xpath("//div[@id='pagination']/span/text()")[0] # Page X of Y
    pages_count = int(re.match(r'^Page \d+ of (\d+)$', pagination_span).group(1))
    assert pages_count == expected_pages


def assert_rows_count(tree, expected_count: int) -> None:
    table_row_count = len(tree.xpath("//table/tbody/tr"))
    assert table_row_count == expected_count


def assert_total_users(tree, expected_amount: int) -> None:
    assert_field_by_data_id(tree, 'total-users-amount', expected_amount)
