from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import (
    get_unique_short_id,
    is_valid_custom_short_id,
    is_short_id_exists
)


@app.route('/api/id/<short_id>', methods=('GET',))
@app.route('/api/id/<short_id>/', methods=('GET',))
def get_url(short_id):
    if not short_id:
        return (
            jsonify({'message': 'Отсутствует короткая ссылка'}),
            HTTPStatus.BAD_REQUEST
        )

    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        return (
            jsonify({'message': 'Указанный id не найден'}),
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    if not request.is_json:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    original_url = data['url']
    custom_id = data.get('custom_id')

    if custom_id is not None and not custom_id:
        custom_id = None

    if custom_id is not None and is_short_id_exists(custom_id):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')

    if custom_id is not None and not is_valid_custom_short_id(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    short_id = custom_id if custom_id is not None else get_unique_short_id()

    url_map = URLMap(original=original_url, short=short_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': f'{request.host_url}{url_map.short}',
    }), HTTPStatus.CREATED
