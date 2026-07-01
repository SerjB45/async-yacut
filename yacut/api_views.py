from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, is_valid_custom_short_id


@app.route('/api/id/<short_id>', methods=('GET',))
def get_url(short_id):
    if not short_id:
        return (
            jsonify({'error': 'Отсутствует короткая ссылка'}),
            HTTPStatus.BAD_REQUEST
        )

    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        return (
            jsonify({'error': 'Ссылка не найдена'}),
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK    


@app.route('/api/id/', methods=('POST',))
def create_short_link(): 
    
    data = request.get_json()
    if not data or 'url' not in data:
        raise InvalidAPIUsage('Отсутствует обязательный параметр: url')

    original_url = data['url']
    custom_id = data.get('custom_id')

    if custom_id and not is_valid_custom_short_id(custom_id):
        raise InvalidAPIUsage('Недопустимый пользовательский идентификатор')

    short_id = custom_id if custom_id else get_unique_short_id()

    url_map = URLMap(original=original_url, short=short_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
       