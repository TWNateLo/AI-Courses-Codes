from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryMemory, FileChatMessageHistory

chat = ChatOpenAI()

memory = ConversationSummaryMemory(
    chat_memory=FileChatMessageHistory("messages.json"), 
    memory_key="messages", 
    return_messages=True,
    llm=chat
)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(prompt=prompt, llm=chat, memory=memory, verbose=True)

while True:
    content = input(">>")

    result = chain({"content": content})

    print(result["text"])