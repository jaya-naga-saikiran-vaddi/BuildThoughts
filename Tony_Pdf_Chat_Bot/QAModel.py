from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class QAModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.prompt_template = """You are a helpful assistant answering questions based on the provided PDF document. 
        Use only the following context to answer the question. If the answer is not in the context, say so clearly. 
        Context: {context} Question: {question} Answer:"""
        self.prompt = PromptTemplate(template=self.prompt_template, input_variables=["context", "question"])
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-3.5-turbo"
        )

    def createQaChain(self, retriever):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": self.prompt}
        )
