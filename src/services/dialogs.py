from typing import List

from fastapi import HTTPException, status
from fastapi.params import Depends
from langchain_core.messages import HumanMessage, AIMessage

from repositories.dialogs import DialogRepository
from schemas.dialogs import MessageSchema, AskQuestionSchema, DialogSchema
from utils.langchain import initialize_langchain


class DialogService:
    def __init__(self, repo: DialogRepository = Depends()):
        self.repo = repo
        self.langchain_chain = initialize_langchain()

    async def create(self, user_id: str):
        return await self.repo.create(user_id)

    async def get(self, user_id: str, dialog_id: str) -> DialogSchema:
        dialog = await self.repo.get(user_id, dialog_id)
        if not dialog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dialog not found')
        return dialog

    async def list(self, user_id: str) -> List[DialogSchema]:
        return await self.repo.list(user_id)

    async def delete(self, user_id: str, dialog_id: str):
        dialog = await self.repo.get(user_id, dialog_id)
        if not dialog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dialog not found')

        return await self.repo.delete(user_id, dialog_id)

    async def ask_question(self, user_id: str, dialog_id: str, payload: AskQuestionSchema) -> MessageSchema:
        dialog = await self.repo.get(user_id, dialog_id)
        if not dialog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dialog not found')

        messages = []
        for message in dialog.messages:
            messages.append(HumanMessage(content=message["question"]))
            messages.append(AIMessage(content=message["answer"]))

        self.langchain_chain.memory.chat_memory.messages = messages

        try:
            ai_response = self.langchain_chain.predict(input=payload.question)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"LangChain error: {str(e)}")

        new_message = MessageSchema(question=payload.question, answer=ai_response)

        await self.repo.update(user_id, dialog_id, new_message)

        return new_message
