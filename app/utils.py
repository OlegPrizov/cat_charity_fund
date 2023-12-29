from datetime import datetime

from app.models.sample_model import DonationAndCharityProjectBaseModel


def investing(
    target: DonationAndCharityProjectBaseModel,
    sources: list[DonationAndCharityProjectBaseModel]
) -> list[DonationAndCharityProjectBaseModel]:
    changed_obj = []
    for source in sources:
        if target.full_amount <= 0:
            break
        amount_to_invest = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += amount_to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        changed_obj.append(source)
    return changed_obj