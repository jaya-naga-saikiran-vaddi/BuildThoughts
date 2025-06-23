from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from mcp_handler import MCPContextBuilder, to_prompt

class mcpModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-4-turbo"
        )
        self.mcp = MCPContextBuilder(
            task="Generate SQL or answer user queries based on the PDF",
            output_format="SQL DDL + INSERT statements OR paragraph answer depending on question",
            guidelines=[
                "Use only the provided context",
                "Do not hallucinate data",
                "Output valid SQL if requested",
                "Give clean readable answers"
            ]
        )

    def ask(self, retriever, document_chunks, question):
        context_data = self.mcp.build_context(document_chunks, question)
        prompt = to_prompt(context_data)
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )
        return qa_chain.run(question)
