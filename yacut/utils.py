import random
import string

from sqlalchemy.exc import OperationalError

from . import db
from .models import URLMap, LENGTH_SHORT_URL

ALLOWED_CHARS = string.ascii_letters + string.digits


def get_unique_short_id(length=6):
    reserved_ids = {'files'}

    numb_attempts = 0
    while True:
        numb_attempts += 1
        short_id = ''.join(random.choice(ALLOWED_CHARS) for _ in range(length))
        if short_id in reserved_ids:
            continue
        if not is_short_id_exists(short_id):
            return short_id
        if numb_attempts > 10:
            raise TimeoutError('Ошибка при генерации короткой ссылки')


def is_short_id_exists(short_id):
    try:
        return db.session.query(URLMap.id).filter_by(
            short=short_id
        ).first() is not None
    except OperationalError:
        return False


def is_valid_custom_short_id(custom_id):
    if not custom_id or len(custom_id) > LENGTH_SHORT_URL:
        return False

    if custom_id == 'files':
        return False

    if is_short_id_exists(custom_id):
        return False

    if not all(c in ALLOWED_CHARS for c in custom_id):
        return False

    return True
