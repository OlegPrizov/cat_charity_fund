from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

Model = TypeVar('Model', bound=Base)
Schema = TypeVar('Schema', bound=BaseModel)


class CRUDBase(Generic[Model, Schema]):

    def __init__(self, model: Model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: Schema,
            session: AsyncSession,
            commit: bool = True,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['invested_amount'] = 0
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: Model,
            obj_in: Schema,
            session: AsyncSession,
            commit: bool = True
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: Model,
            session: AsyncSession
    ) -> Optional[Model]:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_opened_objects(
            self,
            session: AsyncSession
    ) -> list[Optional[Model]]:
        opened_objects = await session.execute(
            select(
                self.model
            ).where(
                not_(self.model.fully_invested)
            ).order_by(
                self.model.create_date
            )
        )
        return opened_objects.scalars().all()
