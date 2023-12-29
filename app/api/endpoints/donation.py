from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.base import CRUDBase as crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.utils import investing

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    })
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    new_donation = await donation_crud.create(
        donation,
        session,
        False,
        user)
    opened_objects = await donation_crud.get_opened_objects(session=session)
    session.add_all(await investing(new_donation, opened_objects))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    })
async def get_all_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    return await donation_crud.get_user_donations(session, user)