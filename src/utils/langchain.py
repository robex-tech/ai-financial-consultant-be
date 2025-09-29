from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               MessagesPlaceholder, SystemMessagePromptTemplate)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from config.settings import settings


def initialize_langchain():
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=settings.open_api_key
    )

    system_template = settings.system_template

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    return conversation
