from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

TEXT_ERROR_EXISTING_NAME = 'Проект с таким именем уже существует!'
TEXT_ERROR_NOT_EXISTING_PROJECT = 'Проект не найден!'
TEXT_ERROR_EDITING_CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'
TEXT_ERROR_FULL_AMOUNT_LESS_INVESTED = (
    'Общая сумма сбора меньше той, что уже собрана!')
TEXT_ERROR_DELETING_PROJECT_WITH_DONATIONS = (
    'В проект были внесены средства, не подлежит удалению!')


async def check_charity_project_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name,
        session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=TEXT_ERROR_EXISTING_NAME)


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=TEXT_ERROR_NOT_EXISTING_PROJECT)
    return charity_project


async def check_charity_project_before_edit(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id,
        session=session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=TEXT_ERROR_EDITING_CLOSED_PROJECT)
    full_amount = obj_in.full_amount
    if full_amount and full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=TEXT_ERROR_FULL_AMOUNT_LESS_INVESTED)
    return charity_project


async def check_charity_project_before_delete(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id,
        session=session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=TEXT_ERROR_DELETING_PROJECT_WITH_DONATIONS)
    return charity_project