from peewee import (
    Proxy,
    Model,
    CharField,
    ForeignKeyField,
    IntegerField,
    TextField,
    DateTimeField
)


db_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class CoordinatesModel(BaseModel):
    latitude = CharField()
    longitude = CharField()


class TimezoneModel(BaseModel):
    offset = CharField()
    description = CharField()


class LocationModel(BaseModel):
    street_number = IntegerField()
    street_name = CharField()
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = CharField()
    coordinates = ForeignKeyField(CoordinatesModel, backref='location')
    timezone = ForeignKeyField(TimezoneModel, backref='location')


class NameModel(BaseModel):
    title = CharField()
    first = CharField()
    last = CharField()


class LoginModel(BaseModel):
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()


class DobModel(BaseModel):
    date = DateTimeField()
    age = IntegerField()


class RegisteredModel(BaseModel):
    date = DateTimeField()
    age = IntegerField()


class IdModel(BaseModel):
    name = CharField()
    value = CharField()


class PictureModel(BaseModel):
    large = TextField()
    medium = TextField()
    thumbnail = TextField()


class User(BaseModel):
    gender = CharField()
    name = ForeignKeyField(NameModel, backref='user')
    location = ForeignKeyField(LocationModel, backref='user')
    email = CharField()
    login = ForeignKeyField(LoginModel, backref='user')
    dob = ForeignKeyField(DobModel, backref='user')
    registered = ForeignKeyField(RegisteredModel, backref='user')
    phone = CharField()
    cell = CharField()
    id_info = ForeignKeyField(IdModel, backref='user')
    picture = ForeignKeyField(PictureModel, backref='user')
    nat = CharField()
