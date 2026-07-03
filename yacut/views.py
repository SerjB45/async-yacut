from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app, db
from .models import URLMap
from .forms import UploadFileForm, ShortUrlForm
from .upload_file_to_ya_disk import async_upload_file_to_yandex_disk


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
        custom_id = form.custom_id.data or None

        if custom_id and URLMap.query.filter_by(short=custom_id).first():
            flash('Пользовательский короткий идентификатор уже существует. '
                  'Пожалуйста, выберите другой.')
            return render_template('index.html', form=form)

        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_map.get_short_url()
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/files', methods=('GET', 'POST'), endpoint='upload_file_view')
def upload_file_view():
    form = UploadFileForm()
    if form.validate_on_submit():
        try:
            urls = async_upload_file_to_yandex_disk(form.files.data)
            return render_template(
                'upload_files.html',
                form=form,
                uploaded_files=[
                    {
                        'name': file.filename,
                        'link': URLMap.create(original=url).get_short_url()
                    }
                    for file, url in zip(form.files.data, urls)
                ]
            )
        except Exception as e:
            flash(f'Ошибка при загрузке файлов: {str(e)}')
            return render_template('upload_files.html', form=form)
    return render_template('upload_files.html', form=form)
