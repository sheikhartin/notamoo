from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from notamoo.database import Base


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(String, nullable=False)
    password = Column(String, nullable=True)
    view_limit = Column(Integer, nullable=True)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    def is_expired(self) -> bool:
        return (
            self.expires_at is not None and self.expires_at <= datetime.utcnow()
        )

    def has_reached_view_limit(self) -> bool:
        return self.view_limit is not None and self.views >= self.view_limit
