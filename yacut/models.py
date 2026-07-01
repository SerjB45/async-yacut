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

    def to_dict(self):
        return {
            'short_link':
                url_for('get_url', short_id=self.short, _external=True),
            'url': self.original,
        }

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
