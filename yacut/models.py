from datetime import datetime, timezone

from flask import url_for

from yacut import db

LENGTH_LONG_URL = 255
LENGTH_SHORT_URL = 16


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LENGTH_LONG_URL), nullable=False)
    short = db.Column(db.String(LENGTH_SHORT_URL), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime,
                          default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return (
            f'<URLMap id={self.id}, original={self.original}, '
            f'short={self.short}, timestamp={self.timestamp}>'
        )

    def get_short_url(self):
        return url_for('short_link_redirect', short=self.short, _external=True)
