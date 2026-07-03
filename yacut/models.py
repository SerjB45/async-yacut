from datetime import datetime, timezone

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(255), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime,
                          default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return (
            f'<URLMap id={self.id}, original={self.original}, '
            f'short={self.short}, timestamp={self.timestamp}>'
        )

    def get_short_url(self):
        return url_for('short_link_redirect', short=self.short, _external=True)
