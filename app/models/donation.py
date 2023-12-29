from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.sample_model import InvestableModel


class Donation(InvestableModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пожертвование. {super().__repr__()},'
            f'{self.user_id=}, {self.comment=})'
        )
