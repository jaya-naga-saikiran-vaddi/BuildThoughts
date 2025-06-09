import Constants
from ChatInterface import ChatInterface, setupSidebar, handleUserInput
from PDFProcessor import PDFProcessor
from QAModel import QAModel
from VectorStoreManager import VectorStoreManager
import streamlit as st


def main():
    chat_interface = ChatInterface()
    file = setupSidebar()

    if file is not None:
        try:
            pdf_processor = PDFProcessor(file)
            pdf_processor.extractText()
            pdf_processor.splitText()

            vector_store_manager = VectorStoreManager(Constants.OPENAI_API_KEY)
            vector_store_manager.createVectorStore(pdf_processor.chunks)

            qa_model = QAModel(Constants.OPENAI_API_KEY)
            retriever = vector_store_manager.getRetriever()
            qa_chain = qa_model.createQaChain(retriever)

            handleUserInput(qa_chain)
            chat_interface.displayChat()

        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
    else:
        st.info("Please upload a PDF file to start.")


if __name__ == "__main__":
    main()
