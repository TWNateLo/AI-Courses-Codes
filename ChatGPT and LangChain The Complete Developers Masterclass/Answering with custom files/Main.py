from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma



embeddings = OpenAIEmbeddings()
#Only need to run for one time at first
#emb = embeddings.embed_query("Hi there")
#print(emb)

text_splitter = CharacterTextSplitter(
    separator = '\n',
    chunk_size = 200,
    chunk_overlap = 0
)

loader=TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="emb"
)

results = db.similarity_search(
    "What is the interesting fact about the English language?",
    #k = 1 #(List the top 2 results)
)

for result in results:
    print("\n")
    print(result.page_content)