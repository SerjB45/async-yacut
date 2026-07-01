import random
import string

from . import db
from .models import URLMap


def get_unique_short_id(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits

    while True:
        short_id = ''.join(random.choice(alphabet) for _ in range(length))
        if not is_short_id_exists(short_id):
            return short_id


def is_short_id_exists(short_id: str) -> bool:
    return db.session.query(URLMap.id).filter_by(
        short=short_id
    ).first() is not None


def is_valid_custom_short_id(custom_id: str) -> bool:
    if not custom_id or len(custom_id) < 3 or len(custom_id) > 16:
        return False

    if is_short_id_exists(custom_id):
        return False

    if not all(c.isalnum() for c in custom_id):
        return False

    return True