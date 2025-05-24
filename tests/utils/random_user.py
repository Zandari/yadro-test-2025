from app import models
from faker import Faker
import uuid
import hashlib
from datetime import datetime

fake = Faker()


def create_random_user() -> models.User:
    global fake

    with models.db_proxy.atomic() as transaction:
        coords = models.CoordinatesModel.create(
            latitude=str(fake.latitude()),
            longitude=str(fake.longitude())
        )

        timezone = models.TimezoneModel.create(
            offset=fake.timezone(),
            description=fake.timezone()
        )

        location = models.LocationModel.create(
            street_number=fake.random_int(1, 9999),
            street_name=fake.street_name(),
            city=fake.city(),
            state=fake.state(),
            country=fake.country_code(),
            postcode=fake.postcode(),
            coordinates=coords,
            timezone=timezone
        )

        name = models.NameModel.create(
            title=fake.prefix(),
            first=fake.first_name(),
            last=fake.last_name()
        )

        salt = fake.sha1()[:8]
        password = fake.password()
        login = models.LoginModel.create(
            uuid=str(uuid.uuid4()),
            username=fake.user_name(),
            password=password,
            salt=salt,
            md5=hashlib.md5(f"{password}{salt}".encode()).hexdigest(),
            sha1=hashlib.sha1(f"{password}{salt}".encode()).hexdigest(),
            sha256=hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        )

        dob_date = fake.date_of_birth()
        dob = models.DobModel.create(
            date=dob_date,
            age=datetime.now().year - dob_date.year
        )

        registered_date = fake.past_datetime()
        registered = models.RegisteredModel.create(
            date=registered_date,
            age=datetime.now().year - registered_date.year
        )

        id_info = models.IdModel.create(
            name=fake.random_element(('SSN', 'PASSPORT', 'DRIVING LICENSE')),
            value=fake.ssn()
        )

        picture = models.PictureModel.create(
            large=fake.image_url(),
            medium=fake.image_url(),
            thumbnail=fake.image_url()
        )

        user = models.User.create(
            gender=fake.random_element(('male', 'female')),
            name=name,
            location=location,
            email=fake.email(),
            login=login,
            dob=dob,
            registered=registered,
            phone=fake.phone_number(),
            cell=fake.phone_number(),
            id_info=id_info,
            picture=picture,
            nat=fake.country_code()
        )

        return user


def create_random_user_in_bulk(amount: int) -> list[models.User]:
    return [create_random_user() for _ in range(amount)]
