from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.sample_model import DonationAndCharityProjectBaseModel


class Donation(DonationAndCharityProjectBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return f'Пожертвование. {super().__repr__()}'
