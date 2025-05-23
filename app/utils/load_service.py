from app.utils.api_client import fetch_users_from_api
from app.utils.parser import ParsedModels, parse_json_users_in_bulk
from app.utils.persister import persist_user


def load_users(amount: int) -> None:
    json_users = fetch_users_from_api(amount=amount)

    parsed_users: list[ParsedModels] = parse_json_users_in_bulk(json_users)

    for p_user in parsed_users:
        persist_user(
            user=p_user.user,
            related_models=p_user.related_models,
        )
