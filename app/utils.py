from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.models.sample_model import DonationAndCharityProjectBaseModel


async def investing(
    session: AsyncSession,
    target: DonationAndCharityProjectBaseModel
) -> list[Optional[DonationAndCharityProjectBaseModel]]:

    crud = (
        charity_project_crud
        if isinstance(target, Donation)
        else donation_crud)
    updated_objects = []
    for source in await crud.get_opened_objects(session):
        amount = min(
            source.full_amount - (source.invested_amount or 0),
            target.full_amount - (target.invested_amount or 0))

        for obj in [target, source]:
            obj.invested_amount = (obj.invested_amount or 0) + amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

        updated_objects.append(source)
        if target.fully_invested:
            break
    return updated_objects