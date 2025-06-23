from typing import List, Dict
from langchain_core.prompts import PromptTemplate


def to_prompt(context: Dict) -> PromptTemplate:
    base_prompt = f"""
You are an intelligent assistant helping with the task: {context['task']}.

Use only the following document chunks to answer the user's question.

Guidelines:
{chr(10).join('- ' + g for g in context['guidelines'])}

Desired output format:
{context['output_format']}

Context:
{{context}}

Question:
{{question}}

Answer:
"""
    return PromptTemplate(
        template=base_prompt,
        input_variables=["context", "question"]
    )


class MCPContextBuilder:
    def __init__(self, task: str, output_format: str, guidelines: List[str]):
        self.task = task
        self.output_format = output_format
        self.guidelines = guidelines

    def build_context(self, document_chunks: List[str], question: str) -> Dict:
        return {
            "role": "pdf_qa_agent",
            "task": self.task,
            "question": question,
            "document_chunks": document_chunks,
            "output_format": self.output_format,
            "guidelines": self.guidelines
        }
