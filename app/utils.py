from datetime import datetime

from app.models.sample_model import DonationAndCharityProjectBaseModel


async def investing(
    target: DonationAndCharityProjectBaseModel, 
    sources: list[DonationAndCharityProjectBaseModel]
):
    objects = []
    if not sources:
        objects.append(target)
        return objects
    for source in sources:
        amount = min(
            source.full_amount - (source.invested_amount),
            target.full_amount - (target.invested_amount))

        for obj in [target, source]:
            obj.invested_amount = (obj.invested_amount) + amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

        objects.append(source)
        if target.fully_invested:
            break
    return objects