from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class QAModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.prompt_template = """
        You are a helpful and intelligent assistant. Use the following context extracted from a PDF document to answer the user's question.
        Only use the given context — do not hallucinate facts.

        You can perform a variety of tasks based on the question, such as:
        - Answering direct questions ,Extracting data into table form
        - Generating SQL schemas and inserts ,Creating summaries or lists
        - Finding insights or comparisons
        If the user asks for a table or SQL, generate structured output accordingly.
        If the answer is not found in the context, clearly say: "I couldn't find that information in the PDF."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

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
