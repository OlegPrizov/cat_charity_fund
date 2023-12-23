from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class TemplateModel(Base):
    __abstract__ = True
    __table_args__ = (CheckConstraint('full_amount >= invested_amount >= 0'),)

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return f'Инвестировано {self.invested_amount} из {self.full_amount}.'