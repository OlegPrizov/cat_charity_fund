from datetime import timedelta
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

GET_REPORT_TO_GOOGLE = 'Добавить данные из БД в Google-таблицу'
TABLE_NAME = 'Отчеты QRkot'
SHEET_NAME_RATING_SPEED_CLOSING = 'Рейтинг проектов по скорости закрытия'

async def spreadsheet_create(wrapper_service: Aiogoogle) -> str:
    service = await wrapper_service.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': TABLE_NAME,
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': SHEET_NAME_RATING_SPEED_CLOSING,
                'gridProperties': {
                    'rowCount': 50,
                    'columnCount': 5
                }
            }}
        ]
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover('drive', 'v3')
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def get_spreadsheet_id(wrapper_service: Aiogoogle) -> str:
    service = await wrapper_service.discover('drive', 'v3')
    response = await wrapper_service.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )
    spreadsheet_id = None
    table = response['files']
    if len(table) > 0:
        for spreadsheet in table:
            if spreadsheet['name'] == TABLE_NAME:
                spreadsheet_id = spreadsheet['id']
                break
    if spreadsheet_id is None:
        spreadsheet_id = spreadsheet_create(
            wrapper_service=wrapper_service
        )
    return spreadsheet_id


async def spreadsheet_update_value(
    spreadsheetid: str,
    projects: List[CharityProject],
    wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('sheets', 'v4')
    await set_user_permissions(
        spreadsheet_id=spreadsheetid,
        wrapper_service=wrapper_service
    )
    table_values = [[
        'Название проекта',
        'Время, затраченное на сбор средств',
        'Описание'
    ]]
    for project in projects:
        table_values.append([
            project.name,
            str(timedelta(project.lifetime)),
            project.description
        ])
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
