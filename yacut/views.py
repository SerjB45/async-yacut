from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app, db
from .forms import ShortUrlForm, UploadFileForm
from .models import URLMap
from .utils import (get_unique_short_id, is_short_id_exists,
                    is_valid_custom_short_id)


@app.route('/<short>', methods=('GET',), endpoint='short_link_redirect')
def redirect_to_short_link(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map:
        return redirect(url_map.original)
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.route('/', methods=('GET', 'POST'), endpoint='short_link_view')
def index_view():
    form = ShortUrlForm()
    short_url = None
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        # Handle empty custom_id
        if custom_id is not None and not custom_id:
            custom_id = None

        # Validate custom_id if provided
        if custom_id is not None:
            # Check for reserved or duplicate IDs
            if custom_id == 'files' or is_short_id_exists(custom_id):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)

            # Check for invalid format (length, characters)
            if not is_valid_custom_short_id(custom_id):
                return render_template('index.html', form=form)

        # Generate short_id if not provided
        short_id = custom_id if custom_id is not None else get_unique_short_id()

        # Create URLMap entry
        url_map = URLMap(original=original_link, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_map.get_short_url()

    return render_template('index.html', form=form, short_url=short_url)


@app.route('/files', methods=('GET', 'POST'), endpoint='upload_file_view')
def upload_file_view():
    form = UploadFileForm()

    return render_template('upload_files.html', form=form)
