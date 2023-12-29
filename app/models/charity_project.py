from sqlalchemy import Column, String, Text

from app.models.sample_model import InvestableModel


class CharityProject(InvestableModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Фонд {self.name}. {super().__repr__()}'
