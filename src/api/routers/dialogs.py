from typing import List

from fastapi import APIRouter, status, Response
from fastapi.params import Depends

from api.dependencies.user import token_dependency, CurrentUser
from schemas.dialogs import AskQuestionSchema, DialogSchema, MessageSchema
from services.dialogs import DialogService

router = APIRouter(
    prefix='/dialogs',
    tags=['dialogs'],
    dependencies=[token_dependency]
)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=DialogSchema
)
async def create_dialog(
        current_user: CurrentUser,
        dialog_service: DialogService = Depends(),
):
    return await dialog_service.create(user_id=current_user.id)


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=List[DialogSchema]
)
async def get_dialogs(
        current_user: CurrentUser,
        dialog_service: DialogService = Depends()
):
    return await dialog_service.list(user_id=current_user.id)


@router.get(
    '/{dialog_id}',
    status_code=status.HTTP_200_OK,
    response_model=DialogSchema
)
async def get_dialog(
        dialog_id: str,
        current_user: CurrentUser,
        dialog_service: DialogService = Depends(),
):
    return await dialog_service.get(user_id=current_user.id, dialog_id=dialog_id)


@router.delete('/{dialog_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_dialog(
        dialog_id: str,
        current_user: CurrentUser,
        dialog_service: DialogService = Depends(),
):
    await dialog_service.delete(user_id=current_user.id, dialog_id=dialog_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/{dialog_id}/ask',
    status_code=status.HTTP_201_CREATED,
    response_model=MessageSchema
)
async def ask_question(
        dialog_id: str,
        payload: AskQuestionSchema,
        current_user: CurrentUser,
        dialog_service: DialogService = Depends(),
):
    return await dialog_service.ask_question(user_id=current_user.id, dialog_id=dialog_id, payload=payload)
