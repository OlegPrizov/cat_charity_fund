from datetime import datetime

from app.models.sample_model import InvestableModel


def investing(
    target: InvestableModel,
    sources: list[InvestableModel]
) -> list[InvestableModel]:
    changed = []
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
        changed.append(source)
    return changed