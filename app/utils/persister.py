from app.models import User, BaseModel, db_proxy


def persist_user(user: User, related_models: list[BaseModel]) -> None:
    with db_proxy.atomic():
        for model in related_models:
            model.save()
        user.save()
