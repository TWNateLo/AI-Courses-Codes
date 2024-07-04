from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

chat = ChatOpenAI()

embeddings = OpenAIEmbeddings()
#Only need to run for one time at first
#emb = embeddings.embed_query("Hi there")
#print(emb)

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

result = chain.run("What is an interesting fact about the English language?")