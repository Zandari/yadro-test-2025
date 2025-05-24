from tests.utils.assertations import assert_field_by_data_id
from tests.utils.detail_fields import DetailDataFieldId
from app.models import User
from lxml import etree
import typing


def test_user_details_view(
    client,
    persisted_user: User,
):
    response = client.get(f'/{persisted_user.id}')
    assert response.status_code == 200

    tree = etree.HTML(response.data)

    assert_field_by_data_id(tree, DetailDataFieldId.USER_ID, persisted_user.id)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_NAME_TITLE, persisted_user.name.title)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_NAME_FIRST, persisted_user.name.first)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_NAME_LAST, persisted_user.name.last)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_GENDER, persisted_user.gender)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_EMAIL, persisted_user.email)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_PHONE, persisted_user.phone)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_CELL, persisted_user.cell)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_STREET_NUMBER, persisted_user.location.street_number)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_STREET_NAME, persisted_user.location.street_name)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_CITY, persisted_user.location.city)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_STATE, persisted_user.location.state)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_COUNTRY, persisted_user.location.country)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_POSTCODE, persisted_user.location.postcode)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LATITUDE, persisted_user.location.coordinates.latitude)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LONGITUDE, persisted_user.location.coordinates.longitude)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_TIMEZONE_OFFSET, persisted_user.location.timezone.offset)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_TIMEZONE_DESCRIPTION, persisted_user.location.timezone.description)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_DOB_DATE, persisted_user.dob.date.strftime('%d.%m.%Y'))
    assert_field_by_data_id(tree, DetailDataFieldId.USER_DOB_AGE, persisted_user.dob.age)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_REGISTERED_DATE, persisted_user.registered.date.strftime('%d.%m.%Y'))
    assert_field_by_data_id(tree, DetailDataFieldId.USER_REGISTERED_AGE, persisted_user.registered.age)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LOGIN_USERNAME, persisted_user.login.username)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LOGIN_PASSWORD, persisted_user.login.password)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LOGIN_UUID, persisted_user.login.uuid)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LOGIN_MD5, persisted_user.login.md5)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LOGIN_SHA1, persisted_user.login.sha1)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_LOGIN_SHA256, persisted_user.login.sha256)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_ID_TYPE, persisted_user.id_info.name)
    assert_field_by_data_id(tree, DetailDataFieldId.USER_ID_NUMBER, persisted_user.id_info.value)
