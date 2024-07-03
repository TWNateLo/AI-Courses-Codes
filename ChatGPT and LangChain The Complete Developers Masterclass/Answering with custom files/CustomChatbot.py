from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma


embeddings = OpenAIEmbeddings()

emb = embeddings.embed_query("Hi there")

print(emb)

text_splitter = CharacterTextSplitter(
    separator = '\n',
    chunk_size = 200,
    chunk_overlap = 0
)

loader=TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

for doc in docs:
    print(doc.page_content)
    print('\n')