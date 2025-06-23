import streamlit as st
import re


def setupSidebar():
    with st.sidebar:
        st.image("PdfChatBot.jpg", caption="Tony : Your  PDF Chatbot Assistant", width=200)
        st.title("Upload Documents Here")
        file = st.file_uploader("Upload a PDF file and start asking questions ", type="pdf")
    return file


def formatResponse(text):
    formatted_text = re.sub(r'(?<!^)(\d+\.)', r'\n\1', text)
    return formatted_text.strip()


def handleUserInput(qa_chain):
    user_question = st.text_input("Ask something about your PDF:")
    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        response = qa_chain.run(user_question)
        st.session_state.chat_history.append({"role": "bot", "content": response})


class ChatInterface:
    def __init__(self):
        self.custom_bot_name = "Tony"
        st.set_page_config(page_title="PDF Chatbot with Tony", layout="wide")
        st.header("Chat with your PDF")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def displayChat(self):
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"**You:** {chat['content']}")
            else:
                formatted_response = formatResponse(chat['content'])
                st.markdown(f"**{self.custom_bot_name}:**\n{formatted_response}")
            st.markdown("---")
