from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, func
from app.core.database import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(String, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Template(id={self.id}, email={self.email})>"

