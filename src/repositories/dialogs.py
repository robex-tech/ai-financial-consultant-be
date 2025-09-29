from typing import List

from beanie import PydanticObjectId

from documents.dialogs import Dialog
from schemas.dialogs import MessageSchema


class DialogRepository:
    async def create(self, user_id: str) -> Dialog:
        new_dialog = Dialog(user_id=user_id, messages=[])
        await new_dialog.create()
        return new_dialog

    async def get(self, user_id: str, dialog_id: str) -> Dialog:
        return await Dialog.find_one(
            Dialog.user_id == user_id,
            Dialog.id == PydanticObjectId(dialog_id)
        )

    async def list(self, user_id: str) -> List[Dialog]:
        return await Dialog.find(Dialog.user_id == user_id)

    async def delete(self, user_id: str, dialog_id: str):
        result = await Dialog.find_one(
            Dialog.user_id == user_id,
            Dialog.id == PydanticObjectId(dialog_id)
        ).delete()
        return result.acknowledged if result else False

    async def update(self, user_id: str, dialog_id: str, new_message: MessageSchema) -> Dialog:
        update_query = (
            await Dialog.find_one(
                Dialog.id == PydanticObjectId(dialog_id),
                Dialog.user_id == user_id
            )
            .update({"$push": {"messages": new_message.model_dump()}})
        )
        return update_query
