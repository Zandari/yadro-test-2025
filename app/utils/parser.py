import json
from app import models
from dataclasses import dataclass
from datetime import datetime
from collections import namedtuple

def _parse_coordinates(json_data: dict) -> models.CoordinatesModel:
    return models.CoordinatesModel(
        latitude=json_data["latitude"],
        longitude=json_data["longitude"]
    )

def _parse_timezone(json_data: dict) -> models.TimezoneModel:
    return models.TimezoneModel(
        offset=json_data["offset"],
        description=json_data["description"]
    )

def _parse_location(
    json_data: dict,
    coordinates: models.CoordinatesModel,
    timezone: models.TimezoneModel,
) -> models.LocationModel:
    return models.LocationModel(
        street_number=int(json_data["street"]["number"]),
        street_name=json_data["street"]["name"],
        city=json_data["city"],
        state=json_data["state"],
        country=json_data["country"],
        postcode=json_data["postcode"],
        coordinates=coordinates,
        timezone=timezone
    )

def _parse_name(json_data: dict) -> models.NameModel:
    return models.NameModel(
        title=json_data["title"],
        first=json_data["first"],
        last=json_data["last"]
    )

def _parse_login(json_data: dict) -> models.LoginModel:
    return models.LoginModel(
        uuid=json_data["uuid"],
        username=json_data["username"],
        password=json_data["password"],
        salt=json_data["salt"],
        md5=json_data["md5"],
        sha1=json_data["sha1"],
        sha256=json_data["sha256"]
    )

def _parse_dob(json_data: dict) -> models.DobModel:
    dob_date = datetime.strptime(
        json_data["date"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return models.DobModel(
        date=dob_date,
        age=int(json_data["age"])
    )

def _parse_registered(json_data: dict) -> models.RegisteredModel:
    registered_date = datetime.strptime(
        json_data["date"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return models.RegisteredModel(
        date=registered_date,
        age=int(json_data["age"])
    )

def _parse_id(json_data: dict) -> models.IdModel:
    return models.IdModel(
        name=json_data["name"],
        value=json_data["value"] or "asdfasdf"
    )

def _parse_picture(json_data: dict) -> models.PictureModel:
    return models.PictureModel(
        large=json_data["large"].strip(),
        medium=json_data["medium"].strip(),
        thumbnail=json_data["thumbnail"].strip()
    )


@dataclass(frozen=True)
class ParsedModels:
    user: models.User
    related_models: tuple


def parse_json_user(json_data: str | dict) -> ParsedModels:
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    name = _parse_name(json_data["name"])
    coordinates=_parse_coordinates(json_data["location"]["coordinates"])
    timezone=_parse_timezone(json_data["location"]["timezone"])
    location = _parse_location(
        json_data["location"],
        coordinates=coordinates,
        timezone=timezone,
    )
    login = _parse_login(json_data["login"])
    dob = _parse_dob(json_data["dob"])
    registered = _parse_registered(json_data["registered"])
    id_info = _parse_id(json_data["id"])
    picture = _parse_picture(json_data["picture"])

    user = models.User(
        gender=json_data["gender"],
        name=name,
        location=location,
        email=json_data["email"],
        login=login,
        dob=dob,
        registered=registered,
        phone=json_data["phone"],
        cell=json_data["cell"],
        id_info=id_info,
        picture=picture,
        nat=json_data["nat"]
    )
    return ParsedModels(
        user=user,
        related_models=(
            name, coordinates, timezone,
            location, login, dob, registered,
            id_info, picture
        )
    )


def parse_json_users_in_bulk(json_data: list[str | dict]) -> list[ParsedModels]:
    result = list()
    for json_user in json_data:
        result.append(parse_json_user(json_user))

    return result
