from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_user_donations(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Optional[Donation]]:
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return reservations.scalars().all()


donation_crud = CRUDDonation(Donation)
