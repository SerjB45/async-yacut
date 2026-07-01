import random
import string

from sqlalchemy.exc import OperationalError

from . import db
from .models import URLMap


def get_unique_short_id(length=6):
    alphabet = string.ascii_letters + string.digits
    reserved_ids = {'files'}

    while True:
        short_id = ''.join(random.choice(alphabet) for _ in range(length))
        if short_id in reserved_ids:
            continue
        if not is_short_id_exists(short_id):
            return short_id


def is_short_id_exists(short_id):
    try:
        return db.session.query(URLMap.id).filter_by(
            short=short_id
        ).first() is not None
    except OperationalError:
        return False


def is_valid_custom_short_id(custom_id):
    if not custom_id or len(custom_id) > 16:
        return False

    if custom_id == 'files':
        return False

    if is_short_id_exists(custom_id):
        return False

    allowed_chars = set(string.ascii_letters + string.digits)
    if not all(c in allowed_chars for c in custom_id):
        return False

    return True