import streamlit as st
import requests

API_URL = "http://localhost:8002/app/v1"


st.set_page_config(
    page_title="TEG AI Assistence",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 TEG AI Assistence")

st.caption("Poweres by RAG + LangGraph")

### Side bar ####

st.sidebar.title("Knowladge Base")

if st.sidebar.button("Start Ingestion"):
    with st.spinner("Building knowladge base..."):
        response = requests.post(f"{API_URL}/start")

        if response.status_code == 200:
            st.sidebar.success("Knowladge base updated")
            st.sidebar.json(response.json)
        else:
            st.sidebar.error(response.text)    


# ------------------------
# Chat
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about TEG..")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content":prompt
        }
    )

with st.chat_message("user"):
    st.markdown(prompt)

with st.chat_message("assistant"):
    placeholder = st.empty()
    placeholder.markdown("Thinking...")

    #
    #Later this call / chat
    #

    response = {
        "answer": "Chat endpoint not implemented yet."
    }
    placeholder.markdown(response["answer"])

st.session_state.messages.append(
    {
        "role":"assistence",
        "content": response["answer"]
    }
)
