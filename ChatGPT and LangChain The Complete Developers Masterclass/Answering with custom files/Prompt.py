from langchain_openai import OpenAIEmbeddings
#The following is deprecated
#from langchain.vectorstores.chroma import Chroma
#This is the correct way to call Chroma now
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

chat = ChatOpenAI()

embeddings = OpenAIEmbeddings()

db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings
)

retriever = db.as_retriever()

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff"
)

"""
result = chain.run("What is an interesting fact about the English language?")
print(result)
"""

#https://github.com/langchain-ai/langchain/discussions/21206
result = chain.invoke("What is an interesting fact about the English language?")
content = result['result']
print(content)