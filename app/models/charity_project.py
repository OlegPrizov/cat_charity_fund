from sqlalchemy import Column, String, Text

from app.models.template_model import TemplateModel


class CharityProject(TemplateModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Фонд {self.name}. {super().__repr__()}'