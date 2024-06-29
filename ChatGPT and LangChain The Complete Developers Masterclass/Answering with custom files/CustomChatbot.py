from langchain.document_loaders import TextLoader

loader=TextLoader("data.txt")
docs = loader.load

print(docs)