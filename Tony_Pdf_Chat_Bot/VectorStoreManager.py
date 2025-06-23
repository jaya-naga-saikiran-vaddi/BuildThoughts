from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class VectorStoreManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.vector_store = None

    def createVectorStore(self, chunks):
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.vector_store = FAISS.from_texts(chunks, embeddings)
        self.vector_store.save_local("faiss_index")

    def getRetriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": 10})
