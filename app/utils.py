from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.models.sample_model import TemplateModel


async def investing(
    session: AsyncSession,
    target: TemplateModel
) -> list[Optional[TemplateModel]]:

    def update_object(
        object: TemplateModel,
        amount: int
    ) -> None:
        object.invested_amount = (object.invested_amount or 0) + amount
        if object.full_amount == object.invested_amount:
            object.fully_invested = True
            object.close_date = datetime.now()

    crud = (
        charity_project_crud
        if isinstance(target, Donation)
        else donation_crud)
    updated_objects = []
    for source in await crud.get_opened_objects(session):
        amount = min(
            source.full_amount - (source.invested_amount or 0),
            target.full_amount - (target.invested_amount or 0))
        update_object(target, amount)
        update_object(source, amount)
        updated_objects.append(source)
        if target.fully_invested:
            break
    return updated_objects
